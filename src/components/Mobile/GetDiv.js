import React, { Component } from "react"
import { InformationProvider, ProductConsumer } from "../../Context"

class GetDiv extends Component {
  render() {
    const {
      value,
      FTUE_Z_ORDER,
      zindexChoice,
      qaLogs,
      elementType,
      clicked,
      showContent,
      hideContent,
      getExperimentsButton,
      updateExperiment,
      id,
      exp_logs,
      addMessage
    } = this.props

//    console.log("&^&^&^&&^&")
//    console.log(getExperimentsButton)

    if (value["zindex"] < FTUE_Z_ORDER && zindexChoice) {
      return
    }
    if (value["zindex"] >= FTUE_Z_ORDER && !zindexChoice) {
      return
    }
    if (!elementType.includes(value["elementType"])) {
//      console.log("OOOOOOOOOOO")
      elementType.push(value["elementType"])
//      console.log(elementType)
    }
    if (value["elementType"] !== "ScrollView" && getExperimentsButton == 0) {
      return (
        <div
          id="element"
          onClick={clicked}
          className="elements"
          onMouseOver={showContent}
          onMouseOut={hideContent}
          value={JSON.stringify(value).replace(/\"/g, "'")}
          datatype={value["elementType"]}
          name={value["name"]}
          style={{
            zIndex: 0,
            position: "absolute",
            border: "solid grey 1px",
            height: value["boundbox"]["height"] + "px",
            width: value["boundbox"]["width"] + "px",
            left: value["boundbox"]["x"] + "px",
            top: value["boundbox"]["y"] + "px"
          }}
        ></div>
      )
    } else if (getExperimentsButton !== 0 && exp_logs.length) {
      var exp_var_ui = ""
      const items = []
//      console.log("In get expppppppppp")
//      console.log(value["variant"])
      for (var k = 0; k < value["variant"].length; k++) {
        var exp_name = value["variant"][k]["name"]
        if (value["chosenVarinat"] === exp_name) {
          items.push(
            <option value={value["variant"][k]["name"]} selected>
              {value["expName"] + "-" + value["variant"][k]["name"]}
            </option>
          )
        } else {
          items.push(
            <option value={value["variant"][k]["name"]}>
              {value["expName"] + "-" + value["variant"][k]["name"]}
            </option>
          )
        }
      }

      return (
        <select
          style={{
            display: "block",
            width: "700px",
            height: "80px",
            marginTop: "10px",
            marginBottom: "5px",
            fontSize:"40px"
          }}
          onChange={updateExperiment}
          id={value["expName"]}
        >
          {items.map((va) => {
            return va
          })}
        </select>
      )
    } else {
      //
      return <p>Hello</p>
    }
  }
}
export default GetDiv

// import React, { Component } from "react"

// const GetDiv = ({
//   id,
//   onClick,
//   className,
//   onMouseOver,
//   onMouseOut,
//   value,
//   data_types,
//   name,
//   zindex,
//   position,
//   width,
//   height,
//   left,
//   top,
//   ...props
// }) => {
//   const styles = {
//     zIndex: "0",
//     position: "absolute",
//     border: "solid grey 1px",
//     width: `${width}px`,
//     height: `${height}px`,
//     left: `${left}px`,
//     top: `${top}px`
//   }
//   return (
//     <div
//       id={id}
//       onClick={onClick}
//       className={className}
//       onMouseOver={onMouseOver}
//       onMouseOut={onMouseOut}
//       value={value}
//       datatype={data_types}
//       name={name}
//       style={styles}
//     ></div>
//   )
// }

// export default GetDiv

// ...this.state.logs,
//           qaLogs: this.qaLogs,
//           clicked: this.clicked,
//           showcontent: this.showcontent,
//          hidecontent: this.hidecontent
