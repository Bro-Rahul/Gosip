import React, { useState } from "react";

import ForgetPasswordForm from "./ForgetPasswordForm";
const LoginUserForm: React.FC<{ toggleForm: React.Dispatch<React.SetStateAction<boolean>> }> = ({ toggleForm }) => {
  
  const [forgetPassword, setForgetPassword] = useState<boolean>(true);
  return (
    <>
      {forgetPassword ?
        <form className='login-with-gosip-container'>
          <p>Sign in with Gosip Account</p>
          <input type="text" name='Username' placeholder='Username' />
          <p></p>
          <input type="email" name='email' placeholder='Email' />
          <p></p>
          <input type="password" placeholder='Password' />
          <p></p>
          <button>Login</button>
          <div className="forget-and-toggle"> 
            <p className='have-account' onClick={() => toggleForm(pre => !pre)}>Create an account! <span>Register </span></p>
            <p><span onClick={()=>setForgetPassword(pre=>!pre)} className="forget-password"> forget Password</span></p>
          </div>
        </form> :
        <ForgetPasswordForm toggle={setForgetPassword}/>
      }
    </>
  )
}
export default LoginUserForm;