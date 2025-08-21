import { LucideIcon } from 'lucide-react'

interface DashboardCardProps {
  title: string
  value: number
  icon: LucideIcon
  color: string
  isLoading?: boolean
}

export function DashboardCard({ title, value, icon: Icon, color, isLoading }: DashboardCardProps) {
  if (isLoading) {
    return (
      <div className="card">
        <div className="animate-pulse">
          <div className="flex items-center space-x-4">
            <div className={`p-3 rounded-lg ${color} opacity-20`}>
              <div className="h-6 w-6 bg-white rounded" />
            </div>
            <div className="flex-1">
              <div className="h-4 bg-gray-200 rounded w-24 mb-2" />
              <div className="h-6 bg-gray-200 rounded w-16" />
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex items-center space-x-4">
        <div className={`p-3 rounded-lg ${color} text-white`}>
          <Icon className="h-6 w-6" />
        </div>
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  )
}
