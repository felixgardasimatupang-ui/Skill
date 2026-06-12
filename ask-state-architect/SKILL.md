---
name: ask-state-architect
description: Mengatur manajemen state kompleks di frontend (Zustand/Redux) serta sinkronisasi datanya dengan server.
triggers: ["state management", "optimistic update", "data sync", "redux", "zustand", "pinia", "state architecture"]
---

# State Architect

Merancang arsitektur state frontend yang skalabel, predictable, dan sinkron dengan server.

<critical_constraints>
- ❌ NO menyimpan server state di global store tanpa cache layer
- ❌ NO optimistic update tanpa rollback logic
- ❌ NO mutation langsung — gunakan immutable patterns
- ✅ WAJIB pisahkan server state vs UI state
- ✅ WAJIB handle loading, error, dan success state
- ✅ WAJIB normalisasi data di store untuk menghindari duplikasi
</critical_constraints>

<heuristics>
- Global UI state (theme, sidebar) → context / provider
- Server cache (data dari API) → React Query / SWR / TanStack Query
- Complex form → local state + zod validation
- Real-time data (chat, notif) → WebSocket + optimistic UI
- Cross-component shared state → Zustand / Pinia (ringan)
- Large enterprise app → Redux Toolkit + RTK Query
</heuristics>

## Purpose

Memastikan state frontend dikelola secara konsisten, performant, dan sinkron dengan server tanpa race condition atau data inconsistency.

## Usage

Gunakan ketika:
- Mendesain arsitektur frontend baru
- Aplikasi memiliki banyak shared state antar komponen
- Perlu optimistic updates untuk UX yang responsif
- Data real-time perlu sinkronisasi dengan server
- State saat ini menyebabkan bug tidak konsisten

### Core Protocol

1. **Kategorikan State**: Server state vs UI state vs URL state
2. **Pilih Tools**: React Query utk server, Zustand/Pinia utk UI, React Router utk URL
3. **Normalisasi**: Flat entities dengan ID reference
4. **Optimistic UI**: Update segera → rollback jika error
5. **Sync Strategy**: Polling, WebSocket, atau Server-Sent Events

## Examples

### Optimistic Update (Zustand + TanStack Query)
```ts
const mutation = useMutation({
  mutationFn: (data) => api.updateUser(data),
  onMutate: async (newData) => {
    await queryClient.cancelQueries({ queryKey: ['user', id] })
    const previous = queryClient.getQueryData(['user', id])
    queryClient.setQueryData(['user', id], newData)
    return { previous }
  },
  onError: (err, newData, context) => {
    queryClient.setQueryData(['user', id], context?.previous)
  },
  onSettled: () => queryClient.invalidateQueries({ queryKey: ['user', id] })
})
```

### Normalized Store (Zustand)
```ts
interface Store {
  entities: { users: Record<string, User> }
  ids: string[]
}

// Selector
const selectUser = (id: string) => (state: Store) => state.entities.users[id]
```

## Best Practices

- **Derived State**: Compute, don't store (`useMemo`)
- **Atomic Updates**: Update related state dalam satu transaction
- **Debounce Sync**: Jangan sync tiap karakter — debounce 300ms
- **Cache Invalidation**: Invalidate query cache setelah mutation sukses
- **DevTools**: Integrasi Redux DevTools / Zustand DevTools
