import React from 'react'

const CreateUserForm: React.FC = () => {
  return (
    <form className='login-with-gosip-container'>
      <p>Sign up with Gosip Account</p>
      <input type="text" name='Username' placeholder='Username' />
      <p></p>
      <input type="email" name='email' placeholder='Email' />
      <p></p>
      <input type="password" placeholder='Password' />
      <p></p>
      <button>Login</button>
    </form>
  )
}

export default CreateUserForm