import React from 'react'
import EmailVerifyForm from './EmailVerifyForm';

const ForgetPasswordForm: React.FC<{toggle:React.Dispatch<React.SetStateAction<boolean>>}> = ({toggle}) => {
    return (
        <form className="login-with-gosip-container">
            <p>Update Your Password</p>
            <EmailVerifyForm inputType='text' title='Username'/>
            <input type="text" placeholder="New Password" />
            <input type="text" placeholder="Comfirm Password" />
            <button>Change Password</button>
            <p className='have-account' onClick={() => toggle(pre => !pre)}>Back to <span>Login </span></p>
        </form>
    );
}
export default ForgetPasswordForm;