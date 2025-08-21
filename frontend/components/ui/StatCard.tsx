import { LucideIcon, TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { cn } from '../../lib/utils'

interface StatCardProps {
  title: string
  value: number
  icon: LucideIcon
  trend?: string
  trendDirection?: 'up' | 'down' | 'neutral'
  color: 'blue' | 'green' | 'purple' | 'orange' | 'red'
}

const colorClasses = {
  blue: 'bg-blue-500 text-blue-600',
  green: 'bg-green-500 text-green-600',
  purple: 'bg-purple-500 text-purple-600',
  orange: 'bg-orange-500 text-orange-600',
  red: 'bg-red-500 text-red-600',
}

const bgColorClasses = {
  blue: 'bg-blue-50',
  green: 'bg-green-50',
  purple: 'bg-purple-50',
  orange: 'bg-orange-50',
  red: 'bg-red-50',
}

export function StatCard({ title, value, icon: Icon, trend, trendDirection, color }: StatCardProps) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <div className={cn("p-3 rounded-lg", bgColorClasses[color])}>
          <Icon className={cn("h-6 w-6", colorClasses[color])} />
        </div>
        {trend && (
          <div className={cn(
            "flex items-center text-sm font-medium",
            trendDirection === 'up' && "text-green-600",
            trendDirection === 'down' && "text-red-600",
            trendDirection === 'neutral' && "text-gray-600"
          )}>
            {trendDirection === 'up' && <TrendingUp className="h-4 w-4 mr-1" />}
            {trendDirection === 'down' && <TrendingDown className="h-4 w-4 mr-1" />}
            {trendDirection === 'neutral' && <Minus className="h-4 w-4 mr-1" />}
            {trend}
          </div>
        )}
      </div>
      
      <div className="mt-4">
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-3xl font-bold text-gray-900 mt-2">{value.toLocaleString()}</p>
      </div>
    </div>
  )
}
