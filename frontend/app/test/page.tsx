'use client'

import { Button } from '../../components/ui/Button'
import { StatCard } from '../../components/ui/StatCard'
import { LoadingSpinner } from '../../components/ui/LoadingSpinner'
import { BookOpen, Users, Calendar } from 'lucide-react'

export default function TestPage() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Component Test Page</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Test Stat"
          value={42}
          icon={BookOpen}
          trend="+10%"
          trendDirection="up"
          color="blue"
        />
      </div>
      
      <div className="space-x-4">
        <Button>Primary Button</Button>
        <Button variant="secondary">Secondary Button</Button>
        <Button variant="outline">Outline Button</Button>
      </div>
      
      <div className="space-x-4">
        <LoadingSpinner size="sm" />
        <LoadingSpinner size="md" />
        <LoadingSpinner size="lg" />
      </div>
    </div>
  )
}
