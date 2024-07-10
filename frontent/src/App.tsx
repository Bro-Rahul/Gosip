import React from 'react'
import { CommentContainer } from 'react-chat'
const App:React.FC = () => {
  return (
    <>
    <CommentContainer post_id='kalki' metaData={{body:'rahul',image:null,title:'this is an title'}}></CommentContainer> 
    </>
  )
}

export default App