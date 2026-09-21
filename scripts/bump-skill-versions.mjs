#!/usr/bin/env node
/**
 * 按提交内容自动更新各 skill 的版本号（写入 skills/<name>/SKILL.md 的 version 字段）。
 *
 * 版本只属于单个 skill，与外层 package.json 的版本无关。
 * bump 级别由 Conventional Commits 推导：fix/其他 -> patch，feat -> minor，BREAKING -> major。
 *
 * 用法：
 *   node scripts/bump-skill-versions.mjs                 依据工作区改动自动判断
 *   node scripts/bump-skill-versions.mjs --staged        只依据暂存区改动（pre-commit 钩子用）
 *   node scripts/bump-skill-versions.mjs --all           所有 skill 都 bump
 *   node scripts/bump-skill-versions.mjs --message "..." 手动指定提交信息
 *   node scripts/bump-skill-versions.mjs --range a..b    指定提交范围（CI 用）
 *   node scripts/bump-skill-versions.mjs --check         校验模式：改了 skill 却没 bump 则退出码 1
 *   node scripts/bump-skill-versions.mjs --dry-run       只打印，不写入
 */

import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS_DIR = path.join(ROOT, "skills");
const INITIAL_VERSION = "0.1.0";

function printHelp() {
  console.log(`按提交内容自动更新各 skill 的版本号

  --range <a..b>        指定 git 提交范围（CI 用）
  --staged              只依据暂存区改动（本地钩子用）
  --all                 所有 skill 都 bump（等同于 --force）
  --message <msg>       手动指定用于推导级别的提交信息
  --check               校验模式：改了 skill 却没 bump 则退出码 1
  --dry-run             只打印，不写入
  --force               即使版本已手动 bump 过也再次 bump
  --no-pre-major-minor  0.x 阶段遇到 BREAKING 也直接升 major（默认降级为 minor）

幂等：若某 skill 的版本相对基线 ref 已经变过，默认跳过，避免本地与 CI 重复 bump。
初始化：基线 ref 里该 skill 还没有 version 字段时按 INIT 处理，保持当前值不加一级
（首次引入版本号属于「初始化」而非「变更」）。加 --force / --all 可强制 bump。`);
}

function parseArgs(argv) {
  const opts = {
    dryRun: false,
    all: false,
    staged: false,
    check: false,
    force: false,
    range: "",
    message: "",
    preMajorMinor: true,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--dry-run") opts.dryRun = true;
    else if (arg === "--all") opts.all = true;
    else if (arg === "--staged") opts.staged = true;
    else if (arg === "--check") opts.check = true;
    else if (arg === "--force") opts.force = true;
    else if (arg === "--no-pre-major-minor") opts.preMajorMinor = false;
    else if (arg === "--range") opts.range = argv[i += 1] ?? "";
    else if (arg === "--message") opts.message = argv[i += 1] ?? "";
    else if (arg === "-h" || arg === "--help") {
      printHelp();
      process.exit(0);
    } else {
      console.error(`未知参数：${arg}`);
      printHelp();
      process.exit(2);
    }
  }
  return opts;
}

function git(args) {
  try {
    return execFileSync("git", args, { cwd: ROOT, encoding: "utf8" }).replace(/\s+$/, "");
  } catch {
    return "";
  }
}

function changedFiles(opts) {
  if (opts.range) {
    return git(["diff", "--name-only", opts.range]).split("\n").filter(Boolean);
  }
  if (opts.staged) {
    return git(["diff", "--cached", "--name-only"]).split("\n").filter(Boolean);
  }
  return git(["status", "--porcelain"])
    .split("\n")
    .filter(Boolean)
    .map((line) => line.slice(3).trim())
    .map((entry) => entry.split(" -> ").pop())
    .map((entry) => entry.replace(/^"|"$/g, ""));
}

function skillFromFile(file) {
  const match = file.replace(/\\/g, "/").match(/^skills\/([^/]+)\//);
  return match ? match[1] : null;
}

function collectMessages(opts) {
  if (opts.message) return [opts.message];
  if (opts.range) {
    const log = git(["log", "--pretty=format:%B%x00", opts.range]);
    return log.split("\u0000").map((item) => item.trim()).filter(Boolean);
  }
  const gitDir = git(["rev-parse", "--absolute-git-dir"]);
  const commitMsgFile = gitDir ? path.join(gitDir, "COMMIT_EDITMSG") : "";
  if (commitMsgFile && existsSync(commitMsgFile)) {
    const content = readFileSync(commitMsgFile, "utf8").trim();
    if (content) return [content];
  }
  const last = git(["log", "-1", "--pretty=%B"]).trim();
  return last ? [last] : [];
}

function levelFromMessage(message) {
  const header = String(message).split("\n")[0];
  if (/^[a-z]+(\([^)]*\))?!:/.test(header) || /BREAKING[ -]CHANGE/.test(String(message))) {
    return 3;
  }
  const type = (header.match(/^([a-z]+)(\([^)]*\))?:/) || [])[1];
  if (type === "feat") return 2;
  return 1;
}

function bumpVersion(current, level, allowPreMajorMinor) {
  const match = /^(\d+)\.(\d+)\.(\d+)/.exec(current);
  if (!match) throw new Error(`无法解析版本号：${current}`);
  const major = Number(match[1]);
  const minor = Number(match[2]);
  const patch = Number(match[3]);
  let effective = level;
  if (allowPreMajorMinor && major === 0 && level === 3) effective = 2;
  if (effective === 3) return `${major + 1}.0.0`;
  if (effective === 2) return `${major}.${minor + 1}.0`;
  return `${major}.${minor}.${patch + 1}`;
}

function readVersion(content) {
  const frontmatter = /^---\r?\n([\s\S]*?)\r?\n---/.exec(content);
  if (!frontmatter) return null;
  const line = /^version:[ \t]*(\S+)[ \t]*(?:#.*)?$/m.exec(frontmatter[1]);
  return line ? line[1] : null;
}

function writeVersion(content, version) {
  const frontmatter = /^---\r?\n([\s\S]*?)\r?\n---/.exec(content);
  if (!frontmatter) throw new Error("SKILL.md 缺少 frontmatter");
  const block = frontmatter[1];
  const next = /^version:[ \t]*\S+.*$/m.test(block)
    ? block.replace(/^version:[ \t]*\S+.*$/m, `version: ${version}`)
    : `${block}\nversion: ${version}`;
  return `---\n${next}\n---${content.slice(frontmatter.index + frontmatter[0].length)}`;
}

function versionAtRef(ref, skill) {
  const raw = git(["show", `${ref}:skills/${skill}/SKILL.md`]);
  return raw ? readVersion(raw) : null;
}

const opts = parseArgs(process.argv.slice(2));

const messages = collectMessages(opts);
const level = messages.reduce((max, message) => Math.max(max, levelFromMessage(message)), 1);
const levelName = { 1: "patch", 2: "minor", 3: "major" }[level];

const skills = opts.all
  ? readdirSync(SKILLS_DIR, { withFileTypes: true })
      .filter((entry) => entry.isDirectory())
      .map((entry) => entry.name)
      .sort()
  : [...new Set(changedFiles(opts).map(skillFromFile).filter(Boolean))].sort();

if (skills.length === 0) {
  console.log("[skill-version] 未检测到 skills/ 下的改动，跳过。");
  process.exit(0);
}

const baseRef = opts.range ? opts.range.split("..")[0] || "HEAD" : "HEAD";
const force = opts.force || opts.all;
const rows = [];
let failed = 0;

for (const skill of skills) {
  const file = path.join(SKILLS_DIR, skill, "SKILL.md");
  if (!existsSync(file)) {
    rows.push([skill, "SKIPPED", "目录下没有 SKILL.md"]);
    continue;
  }

  const content = readFileSync(file, "utf8");
  const current = readVersion(content);

  if (current === null) {
    if (opts.check) {
      rows.push([skill, "FAIL", "frontmatter 缺少 version 字段"]);
      failed += 1;
      continue;
    }
    if (!opts.dryRun) writeFileSync(file, writeVersion(content, INITIAL_VERSION), "utf8");
    rows.push([skill, opts.dryRun ? "DRY-RUN" : "INIT", `新增 version: ${INITIAL_VERSION}`]);
    continue;
  }

  const previous = versionAtRef(baseRef, skill);

  if (opts.check) {
    if (previous && previous === current) {
      rows.push([skill, "FAIL", `内容有改动但版本仍是 ${current}`]);
      failed += 1;
    } else {
      rows.push([skill, "OK", previous ? `${previous} -> ${current}` : current]);
    }
    continue;
  }

  if (!force && !previous) {
    rows.push([skill, "INIT", `基线无 version，保持 ${current}`]);
    continue;
  }

  if (!force && previous !== current) {
    rows.push([skill, "SKIP", `已 bump 过：${previous} -> ${current}`]);
    continue;
  }

  const next = bumpVersion(current, level, opts.preMajorMinor);
  if (!opts.dryRun) writeFileSync(file, writeVersion(content, next), "utf8");
  rows.push([skill, opts.dryRun ? "DRY-RUN" : "BUMPED", `${current} -> ${next}`]);
}

const width = rows.reduce((max, row) => Math.max(max, row[0].length), 0);
for (const [skill, status, detail] of rows) {
  console.log(`[skill-version] ${skill.padEnd(width)}  ${status.padEnd(8)}  ${detail}`);
}
console.log(
  `[skill-version] 级别 ${levelName}${opts.dryRun ? "（dry-run，未写入）" : ""}，来源：${
    messages.length ? messages.join(" | ").split("\n")[0] : "无提交信息，按 patch 处理"
  }`,
);

process.exit(failed > 0 ? 1 : 0);
