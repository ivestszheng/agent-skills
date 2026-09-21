#!/usr/bin/env node
/**
 * 校验各 skill 的 SKILL.md frontmatter 是否满足发布要求（零依赖）。
 *
 * 依据两套规范：
 *   - Agent Skills 开放标准 https://agentskills.io/specification
 *     顶层字段仅 name / description（必填）、license / compatibility / metadata / allowed-tools（可选）
 *   - SkillHub 发布要求 https://skillhub.cn/ai/release.md
 *     必填 slug / displayName / version，建议 summary / tags / license / homepage
 *
 * 用法：
 *   node scripts/validate-skills.mjs            校验全部 skill
 *   node scripts/validate-skills.mjs qianji     只校验指定 skill
 */

import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SKILLS_DIR = path.join(ROOT, "skills");

const STANDARD_REQUIRED = ["name", "description"];
const STANDARD_OPTIONAL = ["license", "compatibility", "metadata", "allowed-tools"];
const PLATFORM_REQUIRED = ["slug", "displayName", "version"];
const PLATFORM_OPTIONAL = ["summary", "tags", "homepage"];
const KNOWN = new Set([
  ...STANDARD_REQUIRED,
  ...STANDARD_OPTIONAL,
  ...PLATFORM_REQUIRED,
  ...PLATFORM_OPTIONAL,
]);

const KEBAB = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const SEMVER = /^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$/;

/** 解析 frontmatter 的顶层键值；块标量（> / |）合并为单行，缩进的嵌套键忽略。 */
function parseFrontmatter(raw) {
  const match = /^---\r?\n([\s\S]*?)\r?\n---/.exec(raw);
  if (!match) return null;
  const fields = {};
  const quoted = new Set();
  let blockKey = null;

  for (const line of match[1].split(/\r?\n/)) {
    const kv = /^([A-Za-z][A-Za-z0-9_-]*):[ \t]*(.*)$/.exec(line);
    if (kv) {
      const [, key, rawValue] = kv;
      const value = rawValue.trim();
      if (value === ">" || value === "|" || value === ">-" || value === "|-") {
        fields[key] = "";
        blockKey = key;
      } else {
        blockKey = null;
        const unquoted = /^(["'])(.*)\1$/.exec(value);
        if (unquoted) quoted.add(key);
        fields[key] = unquoted ? unquoted[2] : value;
      }
      continue;
    }
    if (blockKey && /^[ \t]+\S/.test(line)) {
      fields[blockKey] = fields[blockKey] ? `${fields[blockKey]} ${line.trim()}` : line.trim();
    }
  }
  return { fields, quoted };
}

function checkSkill(dirName) {
  const file = path.join(SKILLS_DIR, dirName, "SKILL.md");
  if (!statSync(file).isFile()) {
    return { dirName, fails: ["目录下没有 SKILL.md"], warns: [] };
  }
  const parsed = parseFrontmatter(readFileSync(file, "utf8"));
  if (!parsed) {
    return { dirName, fails: ["SKILL.md 缺少合法的 YAML frontmatter"], warns: [] };
  }
  const { fields, quoted } = parsed;
  const fails = [];
  const warns = [];

  for (const key of [...STANDARD_REQUIRED, ...PLATFORM_REQUIRED]) {
    if (!fields[key]) fails.push(`缺少 ${key}`);
  }

  if (fields.name) {
    if (fields.name.length > 64) fails.push("name 超过 64 字符");
    if (!KEBAB.test(fields.name)) fails.push(`name 不是 kebab-case：${fields.name}`);
    if (fields.name !== dirName) fails.push(`name 与目录名不一致：${fields.name} != ${dirName}`);
  }
  if (fields.description && fields.description.length > 1024) {
    fails.push(`description 超过 1024 字符（当前 ${fields.description.length}）`);
  }
  if (fields.slug && (!KEBAB.test(fields.slug) || fields.slug.length < 2 || fields.slug.length > 128)) {
    fails.push(`slug 需为 2-128 位 kebab-case：${fields.slug}`);
  }
  if (fields.version && !SEMVER.test(fields.version)) {
    fails.push(`version 不是合法 SemVer：${fields.version}`);
  }
  if (fields.tags && !/^\[.*\]$/.test(fields.tags)) {
    warns.push(`tags 建议写成 YAML 数组：tags: [a, b]（当前为 ${fields.tags}）`);
  }
  if (fields.homepage && !/^https?:\/\/\S+$/.test(fields.homepage)) {
    warns.push(`homepage 建议写成完整的 http(s) 链接：${fields.homepage}`);
  }
  if (fields.compatibility && fields.compatibility.length > 500) {
    fails.push("compatibility 超过 500 字符");
  }
  for (const key of PLATFORM_OPTIONAL) {
    if (!fields[key]) warns.push(`建议补 ${key}`);
  }
  for (const key of Object.keys(fields)) {
    if (!KNOWN.has(key)) warns.push(`非标准顶层字段 ${key}（标准客户端会忽略）`);
  }
  for (const key of quoted) {
    warns.push(`${key} 的值带引号，可以去掉`);
  }

  return { dirName, slug: fields.slug, version: fields.version, fails, warns };
}

function main() {
  if (!existsSync(SKILLS_DIR)) {
    console.error(`找不到 ${SKILLS_DIR}`);
    console.error("本脚本应放在目标仓库的 scripts/ 下运行（仓库根按脚本自身位置推导）。");
    process.exit(1);
  }
  const filter = new Set(process.argv.slice(2).filter((a) => !a.startsWith("-")));
  const dirs = readdirSync(SKILLS_DIR)
    .filter((n) => statSync(path.join(SKILLS_DIR, n)).isDirectory())
    .filter((n) => filter.size === 0 || filter.has(n))
    .sort();

  if (dirs.length === 0) {
    console.error(`没有可校验的 skill（skills/ 下共 ${readdirSync(SKILLS_DIR).length} 项）`);
    process.exit(1);
  }

  const results = dirs.map(checkSkill);
  const seenSlug = new Map();
  for (const r of results) {
    if (!r.slug) continue;
    if (seenSlug.has(r.slug)) r.fails.push(`slug 与 ${seenSlug.get(r.slug)} 重复：${r.slug}`);
    else seenSlug.set(r.slug, r.dirName);
  }

  const width = Math.max(...results.map((r) => r.dirName.length));
  for (const r of results) {
    const status = r.fails.length ? "FAIL" : r.warns.length ? "WARN" : "OK  ";
    const meta = [r.slug && `slug=${r.slug}`, r.version && `v=${r.version}`].filter(Boolean).join("  ");
    console.log(`${status} ${r.dirName.padEnd(width)}  ${meta}`);
    for (const msg of r.fails) console.log(`     ✗ ${msg}`);
    for (const msg of r.warns) console.log(`     ! ${msg}`);
  }

  const failed = results.filter((r) => r.fails.length).length;
  const warned = results.filter((r) => !r.fails.length && r.warns.length).length;
  console.log(
    `\n共 ${results.length} 个 skill：${results.length - failed - warned} 通过，${warned} 有提醒，${failed} 不合规`,
  );
  process.exit(failed ? 1 : 0);
}

main();
