'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { 
  School, 
  Users, 
  BookOpen, 
  Calendar, 
  Plus,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react'
import { api } from '../lib/api'
import { Button } from '../components/ui/Button'
import { toast } from 'react-hot-toast'
import { LoadingSpinner } from '../components/ui/LoadingSpinner'

export default function Dashboard() {
  const [isGenerating, setIsGenerating] = useState(false)

  // Fetch dashboard data
  const { data: summary, isLoading, refetch } = useQuery({
    queryKey: ['dashboard-summary'],
    queryFn: () => api.get('/timetables/school/1/summary').then(res => res.data),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })

  const handleGenerateTimetables = async () => {
    setIsGenerating(true)
    try {
      // Get all classes for the school
      const classesResponse = await api.get('/classes?school_id=1')
      const classIds = classesResponse.data.map((cls: any) => cls.id)
      
      if (classIds.length === 0) {
        toast.error('No classes found. Please add classes first.')
        return
      }

      await api.post('/timetables/generate', {
        class_ids: classIds,
        regenerate: false
      })
      
      toast.success('Timetables generated successfully!')
      refetch() // Refetch data instead of page reload
    } catch (error) {
      console.error('Error generating timetables:', error)
      toast.error('Failed to generate timetables')
    } finally {
      setIsGenerating(false)
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome back! Here's what's happening with your timetables.</p>
        </div>
        <Button
          onClick={handleGenerateTimetables}
          disabled={isGenerating}
          className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white shadow-lg"
        >
          {isGenerating ? (
            <>
              <LoadingSpinner size="sm" className="mr-2" />
              Generating...
            </>
          ) : (
            <>
              <Plus className="h-4 w-4 mr-2" />
              Generate Timetables
            </>
          )}
        </Button>
      </div>

      {/* Simple Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-blue-50">
              <BookOpen className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Classes</p>
              <p className="text-2xl font-bold text-gray-900">{summary?.total_classes || 0}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-green-50">
              <Users className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Active Teachers</p>
              <p className="text-2xl font-bold text-gray-900">{summary?.total_teachers || 0}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-purple-50">
              <Calendar className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Timetables Generated</p>
              <p className="text-2xl font-bold text-gray-900">{summary?.classes_with_timetables || 0}</p>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
          <div className="flex items-center">
            <div className="p-3 rounded-lg bg-orange-50">
              <Clock className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Working Days</p>
              <p className="text-2xl font-bold text-gray-900">{summary?.working_days?.length || 0}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer group">
            <div className="flex items-center space-x-4">
              <div className="p-3 rounded-lg bg-gradient-to-r from-blue-500 to-blue-600 text-white group-hover:scale-110 transition-transform">
                <School className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">Add School</h3>
                <p className="text-sm text-gray-600">Create a new school profile</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer group">
            <div className="flex items-center space-x-4">
              <div className="p-3 rounded-lg bg-gradient-to-r from-green-500 to-green-600 text-white group-hover:scale-110 transition-transform">
                <BookOpen className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 group-hover:text-green-600 transition-colors">Add Class</h3>
                <p className="text-sm text-gray-600">Create a new class</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer group">
            <div className="flex items-center space-x-4">
              <div className="p-3 rounded-lg bg-gradient-to-r from-purple-500 to-purple-600 text-white group-hover:scale-110 transition-transform">
                <Users className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 group-hover:text-purple-600 transition-colors">Add Teacher</h3>
                <p className="text-sm text-gray-600">Add a new teacher</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow cursor-pointer group">
            <div className="flex items-center space-x-4">
              <div className="p-3 rounded-lg bg-gradient-to-r from-orange-500 to-orange-600 text-white group-hover:scale-110 transition-transform">
                <Calendar className="h-6 w-6" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900 group-hover:text-orange-600 transition-colors">View Timetables</h3>
                <p className="text-sm text-gray-600">Browse all timetables</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">System Status</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
              <span className="text-gray-700">Database Connection</span>
            </div>
            <span className="text-green-600 text-sm font-medium">Healthy</span>
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-500 mr-3" />
              <span className="text-gray-700">API Services</span>
            </div>
            <span className="text-green-600 text-sm font-medium">Online</span>
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <AlertCircle className="h-5 w-5 text-yellow-500 mr-3" />
              <span className="text-gray-700">Last Backup</span>
            </div>
            <span className="text-yellow-600 text-sm font-medium">2 hours ago</span>
          </div>
        </div>
      </div>
    </div>
  )
}
