import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import {CommentProvider} from 'react-chat'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
   <CommentProvider client_id='43e70def-a95c-4a4c-920c-b0e93539fc28'>
    <App />
   </CommentProvider>
  </React.StrictMode>,
)
