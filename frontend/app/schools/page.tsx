'use client'

import { useState } from 'react'
import { Plus, Search, Filter, MoreVertical } from 'lucide-react'
import { Button } from '../../components/ui/Button'
import { StatCard } from '../../components/ui/StatCard'
import { LoadingSpinner } from '../../components/ui/LoadingSpinner'

export default function SchoolsPage() {
  const [isLoading, setIsLoading] = useState(false)

  return (
    <div className="p-6 space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Schools</h1>
          <p className="text-gray-600 mt-1">Manage your school profiles and configurations</p>
        </div>
        <Button className="btn-primary">
          <Plus className="h-4 w-4 mr-2" />
          Add School
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Total Schools"
          value={3}
          icon={Plus}
          trend="+1"
          trendDirection="up"
          color="blue"
        />
        <StatCard
          title="Active Schools"
          value={3}
          icon={Plus}
          trend="100%"
          trendDirection="up"
          color="green"
        />
        <StatCard
          title="Total Students"
          value={1250}
          icon={Plus}
          trend="+15%"
          trendDirection="up"
          color="purple"
        />
      </div>

      {/* Search and Filters */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center space-x-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search schools..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
          <Button variant="outline">
            <Filter className="h-4 w-4 mr-2" />
            Filters
          </Button>
        </div>
      </div>

      {/* Schools List */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">All Schools</h3>
        </div>
        
        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <LoadingSpinner size="lg" />
          </div>
        ) : (
          <div className="divide-y divide-gray-200">
            {/* Sample School */}
            <div className="px-6 py-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                    <span className="text-primary-600 font-semibold text-lg">S</span>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">Springfield High School</h4>
                    <p className="text-sm text-gray-600">CBSE Board • 1,250 Students</p>
                  </div>
                </div>
                <Button variant="outline" size="sm">
                  <MoreVertical className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
