import React from "react"
import { useToasts } from "react-toast-notifications"

const Toast = ({ content, alert_called, alert_type, handleClick }) => {
  const { addToast } = useToasts()

  const handle_info = () => {
    {
      addToast(content, {
        appearance: "info",
        autoDismissTimeout: 10000,
        autoDismiss: true
      })
      handleClick()
    }
  }

  const handle_success = () => {
    {
      addToast(content, {
        appearance: "success",
        autoDismissTimeout: 10000,
        autoDismiss: true
      })
      handleClick()
    }
  }

  const handle_error = () => {
    {
      addToast(content, {
        appearance: "error",
        autoDismissTimeout: 10000,
        autoDismiss: true
      })
      handleClick()
    }
  }

  const handle_warning = () => {
    {
      addToast(content, {
        appearance: "warning",
        autoDismissTimeout: 10000,
        autoDismiss: true
      })
      handleClick()
    }
  }

  if (alert_called) {
    console.log(alert_type)
    if (alert_type === "success") {
      return <div onClick={handle_success()}></div>
    }
    if (alert_type === "error") {
      return <div onClick={handle_error()}></div>
    }
    if (alert_type === "warning") {
      return <div onClick={handle_warning()}></div>
    }
    if (alert_type === "info") {
      return <div onClick={handle_info()}></div>
    }
    return null
  } else {
    return null
  }
}

export default Toast
