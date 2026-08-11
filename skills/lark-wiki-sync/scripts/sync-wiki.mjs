#!/usr/bin/env node

/**
 * 将本地 Markdown 文档同步到飞书知识库 wiki 文档。
 *
 * 通用工具：读取项目根目录的 lark-wiki-sync.config.json，
 * 批量将任意 Markdown 文件同步到对应的飞书 wiki 文档。
 *
 * 用法：
 *   node sync-wiki.mjs              # 同步配置中的所有条目
 *   node sync-wiki.mjs --filter 象州  # 只同步名称匹配的条目
 *   node sync-wiki.mjs --dry-run      # 预览，不实际写入
 *   node sync-wiki.mjs --config custom.json  # 指定配置文件
 *
 * 前提：lark-cli 已安装且 bot 已被添加为目标知识库成员。
 */

import { readFileSync, existsSync } from 'node:fs'
import { spawnSync } from 'node:child_process'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

// ---- 从 lark-cli 输出中提取 JSON 对象 ----
function extractJson(output) {
  const match = output.match(/\{[\s\S]*\}/)
  if (match) {
    try {
      return JSON.parse(match[0])
    } catch {
      // ignore
    }
  }
  return null
}

function runLarkCli(args, input) {
  const result = spawnSync('lark-cli', args, {
    input: input || undefined,
    stdio: ['pipe', 'pipe', 'pipe'],
    encoding: 'utf-8',
    shell: process.platform === 'win32',
  })
  const output = (result.stdout || '') + (result.stderr || '')
  return { output, exitCode: result.status }
}

// ---- 解析命令行参数 ----
const args = process.argv.slice(2)
const dryRun = args.includes('--dry-run')
const filterIndex = args.indexOf('--filter')
const filter = filterIndex !== -1 ? args[filterIndex + 1] : null
const configIndex = args.indexOf('--config')
const configName = configIndex !== -1 ? args[configIndex + 1] : 'lark-wiki-sync.config.json'

// ---- 查找配置文件：从 cwd 向上查找 ----
function findConfig(name) {
  let dir = process.cwd()
  for (let i = 0; i < 10; i++) {
    const candidate = resolve(dir, name)
    if (existsSync(candidate)) return candidate
    const parent = resolve(dir, '..')
    if (parent === dir) break
    dir = parent
  }
  return null
}

const configPath = findConfig(configName)

if (!configPath) {
  console.error(`找不到配置文件: ${configName}`)
  console.error(`请从项目根目录运行，或在 --config 中指定路径`)
  process.exit(1)
}

const rootDir = dirname(configPath)
const config = JSON.parse(readFileSync(configPath, 'utf-8'))

// ---- 文档列表 ----
let entries = config.docs || []
if (filter) {
  entries = entries.filter((e) => e.name.includes(filter) || e.path.includes(filter))
}

if (entries.length === 0) {
  console.log('没有匹配的条目')
  process.exit(0)
}

// ---- 飞书域名 ----
const feishuDomain = config.feishuDomain || ''
if (!feishuDomain) {
  console.error('配置缺少 feishuDomain 字段（如 "xxx.feishu.cn"）')
  process.exit(1)
}

console.log(`共 ${entries.length} 个文档待同步${dryRun ? '（dry-run 模式）' : ''}\n`)

let successCount = 0
let skipCount = 0
let failCount = 0

for (const entry of entries) {
  const { name, path, wikiToken, title } = entry

  if (!wikiToken) {
    console.log(`skip  ${name} - 未配置 wikiToken，跳过`)
    skipCount++
    continue
  }

  const filePath = resolve(rootDir, path)
  if (!existsSync(filePath)) {
    console.log(`skip  ${name} - ${path} 不存在，跳过`)
    skipCount++
    continue
  }

  // ---- 读取并处理内容 ----
  const raw = readFileSync(filePath, 'utf-8')
  const lines = raw.split('\n')
  const firstHashIndex = lines.findIndex((l) => l.startsWith('# '))
  const docTitle = title || name
  if (firstHashIndex !== -1) {
    lines[firstHashIndex] = `# ${docTitle}`
  }
  // 在标题后插入同步标记，让阅读者知道文档由 AI 自动同步
  const syncTime = new Date().toISOString().replace('T', ' ').slice(0, 19)
  const noticeLine = `> 本文档由 AI 助手自动同步 · 最后更新于 ${syncTime}`
  if (firstHashIndex !== -1) {
    lines.splice(firstHashIndex + 1, 0, '', noticeLine, '')
  } else {
    lines.unshift(noticeLine, '')
  }
  const content = lines.join('\n')

  // ---- 解析 wiki 节点获取实际 doc token ----
  const { output: nodeOutput, exitCode: nodeExit } = runLarkCli([
    'wiki', '+node-get',
    '--node-token', `https://${feishuDomain}/wiki/${wikiToken}`,
    '--as', 'bot', '--format', 'json',
  ])

  const nodeJson = extractJson(nodeOutput)
  const objToken = nodeJson?.data?.obj_token

  if (!objToken) {
    console.log(`fail   ${name} - 无法解析文档 token (exit=${nodeExit})`)
    console.log(`       ${nodeOutput.slice(0, 300)}`)
    failCount++
    continue
  }

  if (dryRun) {
    console.log(`plan   ${name} -> obj_token=${objToken}`)
    continue
  }

  // ---- 同步文档 ----
  console.log(`sync   ${name} ...`)
  const { output: updateOutput } = runLarkCli([
    'docs', '+update',
    '--doc', objToken,
    '--command', 'overwrite',
    '--doc-format', 'markdown',
    '--content', '-',
    '--as', 'bot',
  ], content)

  const updateJson = extractJson(updateOutput)
  const ok = updateJson?.ok === true
  const resultStatus = updateJson?.data?.result || 'unknown'

  if (ok && resultStatus === 'success') {
    console.log(`ok     ${name} - 同步成功`)
    successCount++
  } else {
    console.log(`fail   ${name} - 同步失败 (${resultStatus})`)
    console.log(`       ${updateOutput.slice(0, 300)}`)
    failCount++
  }
}

console.log(`\n完成：成功 ${successCount}，跳过 ${skipCount}，失败 ${failCount}`)
if (failCount > 0) {
  process.exit(1)
}
