import Link from 'next/link'
import { LucideIcon } from 'lucide-react'
import { cn } from '../../lib/utils'

interface QuickActionCardProps {
  title: string
  description: string
  icon: LucideIcon
  href: string
  color: string
  gradient: string
}

export function QuickActionCard({ title, description, icon: Icon, href, color, gradient }: QuickActionCardProps) {
  return (
    <Link href={href}>
      <div className="group bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-lg transition-all duration-200 cursor-pointer hover:scale-105">
        <div className="flex items-center space-x-4">
          <div className={cn("p-3 rounded-lg bg-gradient-to-r", gradient, "text-white group-hover:scale-110 transition-transform")}>
            <Icon className="h-6 w-6" />
          </div>
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">{title}</h3>
            <p className="text-sm text-gray-600 mt-1">{description}</p>
          </div>
        </div>
      </div>
    </Link>
  )
}
