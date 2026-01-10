import { useState, useCallback } from 'react'
import ReactMarkdown from 'react-markdown'
import { createResearchStream } from '../api/client'

export default function ResearchPage() {
  const [researchType, setResearchType] = useState('company')
  const [companyName, setCompanyName] = useState('')
  const [prospectName, setProspectName] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [loadingStatus, setLoadingStatus] = useState(null)
  const [toolName, setToolName] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = useCallback((e) => {
    e.preventDefault()
    setIsLoading(true)
    setLoadingStatus('thinking')
    setResult(null)
    setError(null)

    const params = researchType === 'company'
      ? { company: companyName }
      : { prospect: prospectName, company: companyName || undefined }

    createResearchStream(researchType, params, 'research', (event) => {
      if (event.type === 'data') {
        const data = event.value

        if (data.status === 'researching') {
          setLoadingStatus('thinking')
        } else if (data.name) {
          setLoadingStatus('tool')
          setToolName(data.name)
        } else if (data.text) {
          setResult(data.text)
        } else if (data.status === 'complete') {
          setIsLoading(false)
          setLoadingStatus(null)
        }
      } else if (event.type === 'error') {
        setError(event.value)
        setIsLoading(false)
        setLoadingStatus(null)
      } else if (event.type === 'done') {
        setIsLoading(false)
        setLoadingStatus(null)
      }
    })
  }, [researchType, companyName, prospectName])

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="px-6 py-4 border-b border-slate-200 bg-white">
        <h2 className="text-lg font-semibold text-slate-900">Research</h2>
        <p className="text-sm text-slate-500">Research companies and prospects for outreach</p>
      </div>

      <div className="flex-1 overflow-y-auto p-6">
        <div className="max-w-2xl mx-auto">
          {/* Research Type Toggle */}
          <div className="flex gap-2 mb-6">
            <button
              onClick={() => setResearchType('company')}
              className={`flex-1 px-4 py-3 rounded-lg font-medium transition-colors ${
                researchType === 'company'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white border border-slate-200 text-slate-600 hover:border-slate-300'
              }`}
            >
              Company Research
            </button>
            <button
              onClick={() => setResearchType('prospect')}
              className={`flex-1 px-4 py-3 rounded-lg font-medium transition-colors ${
                researchType === 'prospect'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white border border-slate-200 text-slate-600 hover:border-slate-300'
              }`}
            >
              Prospect Research
            </button>
          </div>

          {/* Research Form */}
          <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-slate-200 p-6 mb-6">
            {researchType === 'company' ? (
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Company Name
                </label>
                <input
                  type="text"
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                  placeholder="e.g., Anthropic, Stripe, Notion"
                  className="w-full px-4 py-3 border border-slate-300 rounded-lg
                           focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none"
                  required
                />
              </div>
            ) : (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Prospect Name
                  </label>
                  <input
                    type="text"
                    value={prospectName}
                    onChange={(e) => setProspectName(e.target.value)}
                    placeholder="e.g., Dario Amodei, Patrick Collison"
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg
                             focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-2">
                    Company (Optional)
                  </label>
                  <input
                    type="text"
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    placeholder="e.g., Anthropic"
                    className="w-full px-4 py-3 border border-slate-300 rounded-lg
                             focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none"
                  />
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading || (researchType === 'company' ? !companyName : !prospectName)}
              className="mt-6 w-full px-6 py-3 bg-indigo-600 text-white rounded-lg font-medium
                       hover:bg-indigo-700 focus:ring-2 focus:ring-indigo-200 focus:outline-none
                       disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  {loadingStatus === 'tool' ? `Using ${toolName}...` : 'Researching...'}
                </span>
              ) : (
                `Start ${researchType === 'company' ? 'Company' : 'Prospect'} Research`
              )}
            </button>
          </form>

          {/* Error */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
              Error: {error}
            </div>
          )}

          {/* Results */}
          {result && (
            <div className="bg-white rounded-xl border border-slate-200 p-6">
              <h3 className="text-lg font-semibold text-slate-900 mb-4">Research Results</h3>
              <div className="prose prose-slate max-w-none">
                <ReactMarkdown>{result}</ReactMarkdown>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
