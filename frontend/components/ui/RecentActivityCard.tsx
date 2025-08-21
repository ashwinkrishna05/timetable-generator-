import { Plus, Calendar, Users, BookOpen } from 'lucide-react'
import { cn } from '../../lib/utils'

interface RecentActivityCardProps {
  summary?: any
}

export function RecentActivityCard({ summary }: RecentActivityCardProps) {
  const activities = [
    {
      id: 1,
      type: 'timetable',
      message: `${summary?.classes_with_timetables || 0} timetables generated`,
      time: '2 hours ago',
      icon: Calendar,
      color: 'bg-green-100 text-green-600'
    },
    {
      id: 2,
      type: 'teacher',
      message: `${summary?.total_teachers || 0} teachers registered`,
      time: '1 day ago',
      icon: Users,
      color: 'bg-blue-100 text-blue-600'
    },
    {
      id: 3,
      type: 'class',
      message: `${summary?.total_classes || 0} classes created`,
      time: '3 days ago',
      icon: BookOpen,
      color: 'bg-purple-100 text-purple-600'
    }
  ]

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
      <div className="space-y-4">
        {activities.map((activity) => {
          const Icon = activity.icon
          return (
            <div key={activity.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div className={cn("p-2 rounded-lg", activity.color)}>
                  <Icon className="h-4 w-4" />
                </div>
                <div>
                  <p className="font-medium text-gray-900">{activity.message}</p>
                  <p className="text-sm text-gray-600">{activity.time}</p>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
