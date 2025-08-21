'use client'

import { useState, useRef, useEffect } from 'react'
import { LucideIcon } from 'lucide-react'
import { cn } from '../../lib/utils'

interface DropdownItem {
  label: string
  icon: LucideIcon
  onClick: () => void
  className?: string
}

interface DropdownProps {
  trigger: React.ReactNode
  items: DropdownItem[]
}

export function Dropdown({ trigger, items }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  return (
    <div className="relative" ref={dropdownRef}>
      <div onClick={() => setIsOpen(!isOpen)}>
        {trigger}
      </div>
      
      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50">
          {items.map((item, index) => {
            const Icon = item.icon
            return (
              <button
                key={index}
                onClick={() => {
                  item.onClick()
                  setIsOpen(false)
                }}
                className={cn(
                  "w-full flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors",
                  item.className
                )}
              >
                <Icon className="h-4 w-4 mr-3" />
                {item.label}
              </button>
            )
          })}
        </div>
      )}
    </div>
  )
}
