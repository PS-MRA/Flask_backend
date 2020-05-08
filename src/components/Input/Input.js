import React from "react"
import "./Input.css"

const Input = ({
  name,
  type,
  placeholder,
  onChange,
  className,
  value,
  error,
  children,
  label,
  ...props
}) => {
  return (
    <React.Fragment>
      <label htmlFor={name}>{label}</label>
      <input
        id={name}
        name={name}
        type={type}
        placeholder={placeholder}
        onChange={onChange}
        value={value}
        className={className}
      />
    </React.Fragment>
  )
}

Input.defaultProps = {
  type: "text",
  className: "",
  value: ""
}

export default Input
