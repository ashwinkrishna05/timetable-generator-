export default function SimplePage() {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-blue-600">Simple Test Page</h1>
      <p className="text-gray-600 mt-2">This is a basic test page to verify the setup works.</p>
      
      <div className="mt-6 p-4 bg-white rounded-lg shadow border">
        <h2 className="text-xl font-semibold mb-2">Basic Components</h2>
        <button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
          Test Button
        </button>
      </div>
    </div>
  )
}
