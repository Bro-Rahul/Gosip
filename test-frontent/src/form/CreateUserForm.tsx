import React from 'react'
import EmailVerifyForm from './EmailVerifyForm';

const CreateUserForm: React.FC<{toggleForm:React.Dispatch<React.SetStateAction<boolean>>}> = ({toggleForm}) => {
  return (
    <form className='login-with-gosip-container'>
      <p>Sign up with Gosip Account</p>
      <input type="text" name='Username' placeholder='Username' />
      <p></p>
      <EmailVerifyForm inputType='email' title='Email'/>
      <p></p>
      <input type="password" placeholder='Password' />
      <p></p>
      <button>Create Account</button>
      <p className='have-account' onClick={()=>toggleForm(pre=>!pre)}>Already have account <span>Login</span></p>
    </form>
  )
}

export default CreateUserForm