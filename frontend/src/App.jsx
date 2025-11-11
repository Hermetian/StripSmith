import { useState, useEffect } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [step, setStep] = useState('keys') // 'keys', 'upload', 'processing', 'complete'
  const [sessionId, setSessionId] = useState(null)
  const [jobId, setJobId] = useState(null)

  // API Keys
  const [openaiKey, setOpenaiKey] = useState('')
  const [anthropicKey, setAnthropicKey] = useState('')
  const [keysError, setKeysError] = useState('')

  // Story upload
  const [storyFile, setStoryFile] = useState(null)
  const [style, setStyle] = useState('')
  const [chapters, setChapters] = useState('all')
  const [outputFormat, setOutputFormat] = useState('pdf')
  const [uploadError, setUploadError] = useState('')

  // Progress
  const [progress, setProgress] = useState(0)
  const [stage, setStage] = useState('')
  const [downloadUrl, setDownloadUrl] = useState(null)
  const [error, setError] = useState('')

  // Poll for job status
  useEffect(() => {
    if (!jobId || step !== 'processing') return

    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch(`${API_URL}/api/status/${jobId}`)
        const data = await response.json()

        setProgress(data.progress || 0)
        setStage(data.stage || '')

        if (data.status === 'completed') {
          setDownloadUrl(`${API_URL}/api/download/${jobId}`)
          setStep('complete')
          clearInterval(pollInterval)
        } else if (data.status === 'failed') {
          setError(data.error || 'Generation failed')
          setStep('upload')
          clearInterval(pollInterval)
        }
      } catch (err) {
        console.error('Error polling status:', err)
      }
    }, 2000) // Poll every 2 seconds

    return () => clearInterval(pollInterval)
  }, [jobId, step])

  const handleSetKeys = async (e) => {
    e.preventDefault()
    setKeysError('')

    // Basic validation
    if (!openaiKey.startsWith('sk-')) {
      setKeysError('Invalid OpenAI API key format (should start with sk-)')
      return
    }
    if (!anthropicKey.startsWith('sk-ant-')) {
      setKeysError('Invalid Anthropic API key format (should start with sk-ant-)')
      return
    }

    try {
      const response = await fetch(`${API_URL}/api/session/set-keys`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          openai_api_key: openaiKey,
          anthropic_api_key: anthropicKey
        })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to set API keys')
      }

      const data = await response.json()
      setSessionId(data.session_id)
      setStep('upload')
    } catch (err) {
      setKeysError(err.message)
    }
  }

  const handleGenerate = async (e) => {
    e.preventDefault()
    setUploadError('')
    setError('')

    if (!storyFile) {
      setUploadError('Please select a story file')
      return
    }

    try {
      const formData = new FormData()
      formData.append('session_id', sessionId)
      formData.append('story_file', storyFile)
      formData.append('style', style || '')
      formData.append('chapters', chapters)
      formData.append('output_format', outputFormat)

      const response = await fetch(`${API_URL}/api/generate`, {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Failed to start generation')
      }

      const data = await response.json()
      setJobId(data.job_id)
      setStep('processing')
    } catch (err) {
      setUploadError(err.message)
    }
  }

  const handleReset = () => {
    setStep('keys')
    setSessionId(null)
    setJobId(null)
    setOpenaiKey('')
    setAnthropicKey('')
    setStoryFile(null)
    setStyle('')
    setProgress(0)
    setStage('')
    setDownloadUrl(null)
    setError('')
  }

  return (
    <div className="app">
      <header>
        <h1>📚 StripSmith</h1>
        <p className="tagline">AI Comic Generation from Stories</p>
      </header>

      <main>
        {step === 'keys' && (
          <div className="card">
            <h2>Step 1: Enter API Keys</h2>
            <p className="info">
              Your API keys are stored securely in memory only and never saved to disk.
              They expire after 2 hours.
            </p>

            <form onSubmit={handleSetKeys}>
              <div className="form-group">
                <label htmlFor="openai-key">OpenAI API Key</label>
                <input
                  id="openai-key"
                  type="password"
                  placeholder="sk-..."
                  value={openaiKey}
                  onChange={(e) => setOpenaiKey(e.target.value)}
                  required
                />
                <small>Used for DALL-E 3 image generation</small>
              </div>

              <div className="form-group">
                <label htmlFor="anthropic-key">Anthropic API Key</label>
                <input
                  id="anthropic-key"
                  type="password"
                  placeholder="sk-ant-..."
                  value={anthropicKey}
                  onChange={(e) => setAnthropicKey(e.target.value)}
                  required
                />
                <small>Used for Claude story analysis</small>
              </div>

              {keysError && <div className="error">{keysError}</div>}

              <button type="submit" className="btn btn-primary">
                Continue →
              </button>
            </form>
          </div>
        )}

        {step === 'upload' && (
          <div className="card">
            <h2>Step 2: Upload Story & Configure</h2>

            <form onSubmit={handleGenerate}>
              <div className="form-group">
                <label htmlFor="story-file">Story File (TXT)</label>
                <input
                  id="story-file"
                  type="file"
                  accept=".txt"
                  onChange={(e) => setStoryFile(e.target.files[0])}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="style">Art Style (optional)</label>
                <input
                  id="style"
                  type="text"
                  placeholder="e.g., noir comic, manga, superhero comic"
                  value={style}
                  onChange={(e) => setStyle(e.target.value)}
                />
                <small>Leave blank to auto-detect from story</small>
              </div>

              <div className="form-group">
                <label htmlFor="chapters">Chapters</label>
                <input
                  id="chapters"
                  type="text"
                  placeholder="all"
                  value={chapters}
                  onChange={(e) => setChapters(e.target.value)}
                />
                <small>Examples: "all", "1-3", "1"</small>
              </div>

              <div className="form-group">
                <label htmlFor="format">Output Format</label>
                <select
                  id="format"
                  value={outputFormat}
                  onChange={(e) => setOutputFormat(e.target.value)}
                >
                  <option value="pdf">PDF</option>
                  <option value="png">PNG Images</option>
                  <option value="cbz">CBZ (Comic Book)</option>
                </select>
              </div>

              {uploadError && <div className="error">{uploadError}</div>}
              {error && <div className="error">{error}</div>}

              <div className="button-group">
                <button type="button" className="btn btn-secondary" onClick={handleReset}>
                  ← Back
                </button>
                <button type="submit" className="btn btn-primary">
                  Generate Comic
                </button>
              </div>
            </form>

            <div className="cost-info">
              <h3>Cost Estimate</h3>
              <p>Typical 30-panel chapter: ~$1.50-2.00</p>
              <ul>
                <li>Character sheets: ~$0.36</li>
                <li>Panels: ~$1.20</li>
                <li>Claude analysis: ~$0.05</li>
              </ul>
            </div>
          </div>
        )}

        {step === 'processing' && (
          <div className="card">
            <h2>Generating Your Comic...</h2>

            <div className="progress-container">
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              <div className="progress-text">{progress}%</div>
            </div>

            <div className="stage-info">
              <p>{stage}</p>
            </div>

            <div className="info">
              This may take 5-10 minutes depending on story length.
              You can safely close this page and come back later.
            </div>

            <div className="stages-list">
              <div className={progress >= 5 ? 'stage-done' : 'stage-pending'}>
                ✓ Stage 0: Normalize story
              </div>
              <div className={progress >= 10 ? 'stage-done' : 'stage-pending'}>
                ✓ Stage 1: Analyze structure
              </div>
              <div className={progress >= 30 ? 'stage-done' : 'stage-pending'}>
                ✓ Stage 2: Generate character sheets
              </div>
              <div className={progress >= 45 ? 'stage-done' : 'stage-pending'}>
                ✓ Stage 3: Break into panels
              </div>
              <div className={progress >= 90 ? 'stage-done' : 'stage-pending'}>
                ✓ Stage 4: Generate panel images
              </div>
              <div className={progress >= 97 ? 'stage-done' : 'stage-pending'}>
                ✓ Stage 5: Compose pages
              </div>
            </div>
          </div>
        )}

        {step === 'complete' && (
          <div className="card">
            <h2>✨ Comic Complete!</h2>

            <div className="success">
              Your comic has been generated successfully.
            </div>

            <a
              href={downloadUrl}
              className="btn btn-primary btn-large"
              download
            >
              Download Comic
            </a>

            <button
              className="btn btn-secondary"
              onClick={handleReset}
              style={{ marginTop: '1rem' }}
            >
              Generate Another Comic
            </button>
          </div>
        )}
      </main>

      <footer>
        <p>
          <strong>Note:</strong> This is a demo/testing version. You must provide your own API keys.
        </p>
        <p>
          <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener">
            Get OpenAI API Key
          </a>
          {' | '}
          <a href="https://console.anthropic.com/" target="_blank" rel="noopener">
            Get Anthropic API Key
          </a>
        </p>
      </footer>
    </div>
  )
}

export default App
