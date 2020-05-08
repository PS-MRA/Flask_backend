import React, { Component } from "react"
import Button from "../Button/Button"
import Input from "../Input/Input"
import "./Options.css"
import { ProductConsumer } from "../../Context"

class Options extends Component {
  state = {
    cashUpdate: "",
    puzCompleted: ""
  }
  qaLogs = () => console.log("qaLogs")
  clearOutput = () => console.log("Clear")
  getExperiments = () => console.log("getExperiments")
  getAppiumStatus = () => console.log("Appium status")
  gameCommandList = () => console.log("Game command list")

  handleChange = (event) => {
    console.log(event.target.name)
    console.log(this.state.cashUpdate)
    console.log(this.state.puzCompleted)
    this.setState({
      [event.target.name]: event.target.value
    })
  }
  
  render() {
    const {
      qaLogs,
      clearoutput,
      getExperiments,
      getAppiumStatus,
      gameCommandList,
      startRecord,
      stopRecord,
      playRunButton,
      appium_status,
      startAppium
    } = this.props
    var handler =""
    if (appium_status === "Check Appium Connection"){
      handler = getAppiumStatus
    }else{
      handler = startAppium
    }
      return (
        <nav className="options">
          <Button
            onClick={qaLogs}
            id="qaLogs"
            type="button"
            buttonSize="btn--medium"
            buttonStyle="btn--danger--outline"
          >
            qaLogs
          </Button>
          <Button
            onClick={clearoutput}
            id="clear"
            type="button"
            buttonSize="btn--medium"
            buttonStyle="btn--danger--outline"
          >
            Clear
          </Button>
          <Button
            onClick={getExperiments}
            id="getExperiments"
            type="button"
            buttonSize="btn--medium"
            buttonStyle="btn--danger--outline"
          >
            Experiments
          </Button>

          <Button
            onClick={handler}
            id="getAppiumStatus"
            type="button"
            buttonSize="btn--medium"
            buttonStyle="btn--danger--outline"
          >
            {appium_status}
          </Button>

          <Button
            onClick={gameCommandList}
            id="gameCommandList"
            type="button"
            buttonSize="btn--medium"
            buttonStyle="btn--danger--outline"
          >
            Game commands
          </Button>

          <h1>Server Responses</h1>

          {/* Server Response */}
          <Button
            onClick={startRecord}
            type="button"
            name="startRecord"
            id="startRecord"
            buttonSize="btn--medium"
            buttonStyle="btn--danger--outline"
          >
            Start Record
          </Button>
          <Button
            onClick={stopRecord}
            type="button"
            name="stopRecord"
            id="stopRecord"
            buttonSize="btn--medium"
            buttonStyle="btn--danger--outline"
          >
            Stop record
          </Button>

          <Button
            onClick={playRunButton}
            type="button"
            name="playRunButton"
            id="playRunButton"
            buttonSize="btn--medium"
            buttonStyle="btn--danger--outline"
          >
            Play Run
          </Button>
          {/* Dont know why we use */}
          <Input
            name="puzCompleted"
            type="text"
            id="puzCompleted"
            className="input-space"
            onChange={this.handleChange}
            value={this.state.puzCompleted}
          ></Input>

          <Button
            type="button"
            name="puzCompletedBtn"
            id="puzCompletedBtn"
            buttonSize="btn--medium"
            buttonStyle="btn--danger--outline"
          >
            Update PuzCompleted
          </Button>

          {/* Dont know why we use */}
          <Input
            name="cashUpdate"
            type="text"
            id="cashUpdate"
            className="input-space"
            onChange={this.handleChange}
            value={this.state.cashUpdate}
          ></Input>

          <Button
            type="button"
            name="cashUpdateBtn"
            id="cashUpdateBtn"
            buttonSize="btn--medium"
            buttonStyle="btn--danger--outline"
          >
            Update Cash
          </Button>
          <input
            onClick={this.handleChange}
            type="checkbox"
            id="zindex"
            name="zindex"
            checked
          />
          <label htmlFor="male">Zindex Filter</label>
        </nav>
      )
  }
}

export default Options
