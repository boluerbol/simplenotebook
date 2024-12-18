import './styles/index.css'
import Button from '../shared/ui/Button/Button'

function App() {
  return (
    <div className='min-h-screen bg-gray-100'>
      <div className='container mx-auto px-4 py-8'>
        <h1 className='text-4xl font-bold text-gray-900'>
          Vite + React + Tailwind + FSD
        </h1>
        <p className='mt-4 text-gray-600'>
          Edit src/app/index.jsx and save to test HMR
        </p>
        <div className='mt-8 space-x-4'>
          <Button>Default Button</Button>
          <Button variant='secondary'>Secondary Button</Button>
          <Button variant='outline'>Outline Button</Button>
        </div>
        <div className='mt-4 space-x-4'>
          <Button size='sm'>Small Button</Button>
          <Button size='md'>Medium Button</Button>
          <Button size='lg'>Large Button</Button>
        </div>
      </div>
    </div>
  )
}

export default App
