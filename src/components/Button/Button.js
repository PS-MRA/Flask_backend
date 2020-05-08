import React from "react"
import "./Button.css"

const STYLES = [
  "btn--primary--solid",
  "btn--warning--solid",
  "btn--danger--solid",
  "btn--success--solid",
  "btn--primary--outline",
  "btn--warning--outline",
  "btn--danger--outline",
  "btn--success--outline",
  "btn--black--border"
]

const SIZES = ["btn--medium", "btn--large"]

const Button = ({ children, type, onClick, buttonStyle, buttonSize, id }) => {
  const checkButtonStyle = STYLES.includes(buttonStyle)
    ? buttonStyle
    : STYLES[0]
  const checkButtonSize = SIZES.includes(buttonSize) ? buttonSize : SIZES[0]
  return (
    <button
      className={`btn ${checkButtonStyle} ${checkButtonSize}`}
      onClick={onClick}
      id={id}
      type={type}
    >
      {children}
    </button>
  )
}

export default Button
