# Frontend - Next.js Jira Client

Modern Jira client สไตล์ Trello/Linear ด้วย Next.js 14+ และ UI components ที่ทันสมัย
รองรับ drag & drop, real-time updates, และ authentication ผ่าน Jira OAuth 2.0 3LO

## ✨ เทคโนโลยีหลัก

- **Next.js 14+** - React framework พร้อม App Router
- **Auth.js/NextAuth** - Authentication และ session management
- **TanStack Query** - Server state management และ caching
- **dnd-kit** - Drag and drop functionality
- **shadcn/ui** - Modern UI components
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS framework

## 🏗️ โครงสร้างโปรเจกต์

```
frontend/
├─ app/                     # Next.js App Router
│  ├─ (auth)/              # Authentication layouts
│  │  ├─ login/
│  │  └─ callback/
│  ├─ (dashboard)/         # Dashboard layouts
│  │  ├─ board/
│  │  ├─ issues/
│  │  └─ search/
│  ├─ api/                 # API routes
│  │  └─ auth/
│  ├─ globals.css
│  ├─ layout.tsx
│  └─ page.tsx
├─ components/             # Reusable components
│  ├─ ui/                 # shadcn/ui components
│  │  ├─ button.tsx
│  │  ├─ card.tsx
│  │  ├─ dialog.tsx
│  │  └─ ...
│  ├─ board/              # Board-related components
│  │  ├─ board-column.tsx
│  │  ├─ issue-card.tsx
│  │  └─ drag-overlay.tsx
│  ├─ auth/               # Authentication components
│  │  ├─ login-form.tsx
│  │  └─ auth-guard.tsx
│  ├─ layout/             # Layout components
│  │  ├─ header.tsx
│  │  ├─ sidebar.tsx
│  │  └─ navigation.tsx
│  └─ providers/          # Context providers
│     ├─ auth-provider.tsx
│     ├─ query-provider.tsx
│     └─ theme-provider.tsx
├─ lib/                   # Utilities และ configurations
│  ├─ auth.ts            # NextAuth configuration
│  ├─ query-client.ts    # TanStack Query setup
│  ├─ api.ts             # API client
│  ├─ utils.ts           # Utility functions
│  └─ types.ts           # TypeScript types
├─ hooks/                # Custom React hooks
│  ├─ use-jira-api.ts    # Jira API hooks
│  ├─ use-board.ts       # Board state management
│  └─ use-drag-drop.ts   # Drag & drop logic
├─ public/               # Static assets
├─ tailwind.config.js
├─ next.config.js
├─ package.json
├─ tsconfig.json
└─ .env.example
```

## 📦 Dependencies

### Core Dependencies
```json
{
  "next": "^14.0.0",
  "react": "^18.0.0",
  "react-dom": "^18.0.0",
  "typescript": "^5.0.0"
}
```

### UI & Styling
```json
{
  "@radix-ui/react-dialog": "^1.0.5",
  "@radix-ui/react-dropdown-menu": "^2.0.6",
  "@radix-ui/react-select": "^2.0.0",
  "class-variance-authority": "^0.7.0",
  "clsx": "^2.0.0",
  "lucide-react": "^0.294.0",
  "tailwind-merge": "^2.0.0",
  "tailwindcss": "^3.3.0"
}
```

### State Management & Data Fetching
```json
{
  "@tanstack/react-query": "^5.0.0",
  "next-auth": "^4.24.0",
  "zustand": "^4.4.0"
}
```

### Drag & Drop
```json
{
  "@dnd-kit/core": "^6.1.0",
  "@dnd-kit/sortable": "^8.0.0",
  "@dnd-kit/utilities": "^3.2.0"
}
```

## 🚀 การติดตั้งและเริ่มต้น

### 1. ติดตั้ง Dependencies

```bash
cd frontend
npm install
# หรือ
yarn install
# หรือ
pnpm install
```

### 2. ตั้งค่า Environment Variables

```bash
cp .env.example .env.local
```

แก้ไขไฟล์ `.env.local`:

```env
# NextAuth Configuration
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_secret

# Jira OAuth 2.0 3LO
JIRA_CLIENT_ID=your_jira_client_id
JIRA_CLIENT_SECRET=your_jira_client_secret
JIRA_BASE_URL=https://your-domain.atlassian.net

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
API_URL=http://localhost:8000

# Development
NODE_ENV=development
```

### 3. เริ่มต้น Development Server

```bash
npm run dev
# หรือ
yarn dev
# หรือ
pnpm dev
```

แอปพลิเคชันจะพร้อมใช้งานที่: http://localhost:3000

## 🎯 ฟีเจอร์หลัก

### 🔐 Authentication
- Jira OAuth 2.0 3LO integration
- Session management ด้วย NextAuth
- Protected routes และ middleware
- Automatic token refresh

### 📋 Kanban Board
- Drag & drop issues ระหว่างคอลัมน์
- Optimistic updates
- Real-time synchronization
- Custom columns ตาม Jira statuses

### 🔍 Issue Management
- ค้นหาด้วย JQL (Jira Query Language)
- Issue detail view และ editing
- Bulk operations
- Filtering และ sorting

### 🎨 UI/UX
- Responsive design
- Dark/Light theme
- Keyboard shortcuts
- Loading states และ error handling

## 🛠️ การพัฒนา

### การเพิ่ม Component ใหม่

```bash
# สร้าง component ด้วย shadcn/ui
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
```

### การใช้งาน TanStack Query

```typescript
// hooks/use-jira-api.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

export function useIssues(projectKey: string) {
  return useQuery({
    queryKey: ['issues', projectKey],
    queryFn: () => fetchIssues(projectKey),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useUpdateIssue() {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: updateIssue,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['issues'] })
    },
  })
}
```

### การใช้งาน dnd-kit

```typescript
// components/board/board-column.tsx
import { useDroppable } from '@dnd-kit/core'
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable'

export function BoardColumn({ column, issues }) {
  const { setNodeRef } = useDroppable({
    id: column.id,
  })

  return (
    <div ref={setNodeRef} className="flex flex-col gap-2">
      <SortableContext items={issues} strategy={verticalListSortingStrategy}>
        {issues.map(issue => (
          <IssueCard key={issue.id} issue={issue} />
        ))}
      </SortableContext>
    </div>
  )
}
```

## 🎨 การใช้งาน shadcn/ui

### ติดตั้ง shadcn/ui

```bash
npx shadcn-ui@latest init
```

### เพิ่ม Components

```bash
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add select
npx shadcn-ui@latest add toast
```

### ใช้งาน Components

```typescript
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function IssueCard({ issue }) {
  return (
    <Card className="cursor-pointer hover:shadow-md transition-shadow">
      <CardHeader>
        <CardTitle className="text-sm">{issue.key}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground">{issue.summary}</p>
      </CardContent>
    </Card>
  )
}
```

## 🚢 การ Deploy บน Vercel

### 1. เชื่อมต่อ GitHub Repository

1. สร้างบัญชี Vercel.com
2. Import GitHub repository
3. เลือก `frontend` directory

### 2. ตั้งค่า Environment Variables

ใน Vercel dashboard, เพิ่ม environment variables:

```
NEXTAUTH_URL=https://your-app.vercel.app
NEXTAUTH_SECRET=your_production_secret
JIRA_CLIENT_ID=your_jira_client_id
JIRA_CLIENT_SECRET=your_jira_client_secret
JIRA_BASE_URL=https://your-domain.atlassian.net
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
API_URL=https://your-backend.railway.app
NODE_ENV=production
```

### 3. การ Deploy

Vercel จะ deploy อัตโนมัติเมื่อ push code ใหม่

## 🔧 Scripts

```bash
# Development
npm run dev

# Build
npm run build

# Start production server
npm run start

# Lint
npm run lint

# Type check
npm run type-check

# สร้าง component ใหม่
npm run generate:component
```

## 🧪 การทดสอบ

```bash
# Unit tests
npm run test

# E2E tests
npm run test:e2e

# Coverage
npm run test:coverage
```

## 🔍 การ Debug

### Next.js Debug Mode

```bash
NODE_OPTIONS='--inspect' npm run dev
```

### React Developer Tools

ติดตั้ง React Developer Tools extension ในเบราว์เซอร์

### TanStack Query Devtools

```typescript
// app/layout.tsx
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <QueryProvider>
          {children}
          <ReactQueryDevtools initialIsOpen={false} />
        </QueryProvider>
      </body>
    </html>
  )
}
```

## 📚 เอกสารเพิ่มเติม

- [Next.js Documentation](https://nextjs.org/docs)
- [NextAuth.js Documentation](https://next-auth.js.org/)
- [TanStack Query Documentation](https://tanstack.com/query/latest)
- [dnd-kit Documentation](https://dndkit.com/)
- [shadcn/ui Documentation](https://ui.shadcn.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## 🤝 การมีส่วนร่วม

1. Fork repository
2. สร้าง feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit การเปลี่ยนแปลง (`git commit -m 'Add some AmazingFeature'`)
4. Push ไปยัง branch (`git push origin feature/AmazingFeature`)
5. สร้าง Pull Request