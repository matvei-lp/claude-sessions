export const meta = {
  name: 'title-sessions',
  description: 'Generate concise sidebar titles for 42 past CLI sessions from their transcripts',
  phases: [{ title: 'Title' }],
}

const items = typeof args === 'string' ? JSON.parse(args) : args
const TITLE_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: { title: { type: 'string' } },
  required: ['title'],
}

phase('Title')
log(`Titling ${items.length} sessions`)

const results = await parallel(items.map((it, i) => () =>
  agent(
`Read the file ${it.path} — it is the OPENING of a Claude Code coding session (project: ${it.project}). Lines marked [U] are the user, [A] are the assistant.

Write a SHORT session title the way Claude Code auto-titles sessions in its sidebar:
- 3–7 words, max ~50 characters. No trailing period, no surrounding quotes.
- Use the SAME language as the conversation (mostly Russian here; keep English if the session is in English).
- Name the concrete task/topic — not generic words like "помощь" or "session".
- If a Jira key like RMP-XX or RAD-XXXX is clearly the subject, START the title with it (e.g. "RMP-21 переезд на общий make").
- If the session is about a Sentry issue, format as "Sentry: <short topic>" (infer the topic from the discussion, not the raw URL).

Then WRITE the final title (raw text, single line, nothing else) to the file /tmp/rmp_titles/out/${it.cli}.title using the Write tool.
Finally return JSON {"title": "<the title>"}.`,
    { label: `title:${it.project.slice(0,12)}/${it.cli.slice(0,8)}`, phase: 'Title', schema: TITLE_SCHEMA, agentType: 'general-purpose' }
  ).then(r => ({ cli: it.cli, title: r && r.title ? r.title : null }))
))

const ok = results.filter(r => r && r.title).length
log(`Done: ${ok}/${items.length} titled`)
return results