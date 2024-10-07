import  { useState } from 'react'

const EmailVerifyForm:React.FC<{title:string,inputType:string}> = ({title,inputType}) => {
    const [optResend,setOptResend] = useState<boolean>(false);
    const [verifyEmail,setVerifyEmail] = useState<boolean>(false);
  return (
    <form className='email-verification'>
        <input type={inputType} name='email' placeholder={title} disabled={verifyEmail} required/>
        <div>
        {!verifyEmail && <input type="number" placeholder='Enter OTP'/>}
        {!verifyEmail && <button onClick={(e)=>{e.preventDefault(); setOptResend(true);setVerifyEmail(pre=>!pre)}}>{optResend ? "Resend OTP": "Send OTP"}</button>}
        </div>
    </form>
  )
}

export default EmailVerifyForm