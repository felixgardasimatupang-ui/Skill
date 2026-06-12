# N+1 Detection Test

## Input
Prisma query:
```ts
const courses = await prisma.course.findMany()
for (const c of courses) {
  const students = await prisma.student.count({ where: { courseId: c.id } })
}
```

## Expected Output
"Detected N+1 pattern on `prisma.student.count` inside loop. Use `include: { _count: { select: { students: true } } }` instead."
