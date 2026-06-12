---
name: ask-llm-integration-expert
description: Merancang arsitektur fitur berbasis kecerdasan buatan, mengelola efisiensi token, menangani batasan request (rate limiting), serta integrasi database vektor (Vector DB).
triggers: ["llm integration", "ai feature", "vector database", "rag", "semantic search", "token cost", "openai", "langchain"]
---

# LLM Integration Expert

Merancang dan mengimplementasikan fitur AI dengan arsitektur yang skalabel, hemat biaya, dan maintainable.

<critical_constraints>
- ❌ NO hardcode API key — gunakan secrets manager / environment variables
- ❌ NO ekspos raw LLM response ke user tanpa sanitasi
- ❌ NO kirim full konteks ke LLM tanpa chunking
- ✅ WAJIB implementasi rate limiting dan token budgeting
- ✅ WAJIB fallback ketika LLM API down / timeout
- ✅ WAJIB logging prompt + response (tanpa PII) untuk audit
- ✅ WAJIB caching untuk query yang identik
</critical_constraints>

<heuristics>
- Query user similarity → embedding search di Vector DB, bukan LLM setiap kali
- Dokumen panjang → chunking + RAG, bukan kirim semua ke konteks
- Biaya token tinggi → caching semantic + model lebih kecil untuk simple task
- Latency tinggi → streaming response + smaller model fallback
- Hallucination → grounding dengan context + system prompt strict
- Rate limit → queue + retry with exponential backoff
</heuristics>

## Purpose

Memungkinkan integrasi fitur AI/LLM yang aman, hemat biaya, dan mudah dipelihara dengan arsitektur yang tepat.

## Usage

Gunakan ketika:
- Mendesain fitur AI baru (chatbot, search, summarization)
- Integrasi dengan OpenAI / Anthropic / Gemini API
- Setup Vector Database (Pinecone, Qdrant, Weaviate)
- Optimasi biaya token LLM
- Implementasi RAG (Retrieval-Augmented Generation)
- Scaling fitur AI dari prototype ke production

### Core Protocol

1. **Design Flow**: User input → preprocessing → context retrieval → LLM call → postprocessing
2. **Chunking**: Split dokumen menjadi chunks optimal (500-1000 tokens)
3. **Embedding**: Generate embeddings dan simpan di Vector DB
4. **Retrieval**: Semantic search untuk menemukan context relevan
5. **Generation**: Prompt + context → LLM → response
6. **Cost Control**: Cache, token counting, model tiering
7. **Safety**: Content filtering, PII sanitization, rate limiting

## Examples

### RAG Pipeline
```ts
async function answerQuestion(question: string) {
  // 1. Embed question
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: question,
  })

  // 2. Retrieve relevant context
  const results = await vectorDb.query({
    vector: embedding.data[0].embedding,
    topK: 5,
  })

  // 3. Build prompt with context
  const context = results.map(r => r.content).join('\n\n')
  const response = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [
      { role: 'system', content: 'Answer based only on the provided context.' },
      { role: 'user', content: `Context:\n${context}\n\nQuestion: ${question}` },
    ],
    max_tokens: 500,
  })

  return response.choices[0].message.content
}
```

### Token Cost Optimizer
```ts
import { encoding_for_model } from 'tiktoken'

function estimateCost(model: string, text: string): number {
  const enc = encoding_for_model(model)
  const tokens = enc.encode(text).length
  const rates = { 'gpt-4o': { in: 5, out: 15 }, 'gpt-4o-mini': { in: 0.15, out: 0.6 } }
  const r = rates[model]
  return (tokens / 1000) * r.in  // per 1K tokens (input)
}

function chooseModel(complexity: 'simple' | 'complex'): string {
  return complexity === 'simple' ? 'gpt-4o-mini' : 'gpt-4o'
}
```

### Vector DB Integration (Pinecone)
```ts
import { Pinecone } from '@pinecone-database/pinecone'

const pc = new Pinecone({ apiKey: process.env.PINECONE_API_KEY })
const index = pc.index('skill-library')

async function upsertDocument(doc: { id: string, text: string, metadata: any }) {
  const embedding = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: doc.text,
  })
  await index.upsert([{
    id: doc.id,
    values: embedding.data[0].embedding,
    metadata: { text: doc.text, ...doc.metadata },
  }])
}
```

## Best Practices

- **Caching**: Cache embedding + LLM response (TTL sesuai frekuensi perubahan data)
- **Fallback**: Cascading model (gpt-4o → gpt-4o-mini → local model)
- **Monitoring**: Track token usage, cost, latency, error rate
- **Guardrails**: Input validation, output filtering, PII detection
- **A/B Testing**: Uji model berbeda untuk quality vs cost tradeoff
- **Rate Limiting**: Tiered — free user (10 req/hari) vs premium (1000 req/hari)
