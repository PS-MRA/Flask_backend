import React from "react"
import { NotificationContainer, NotificationManager } from "react-notifications"

class Example extends React.Component {
  createNotification = (type) => {
    console.log("In notificatuons")
    console.log(type)
    return () => {
      switch (type) {
        case "info":
          NotificationManager.info("Info message")
          break
        case "success":
          NotificationManager.success("Success message", "Title here")
          break
        case "warning":
          NotificationManager.warning(
            "Warning message",
            "Close after 3000ms",
            3000
          )
          break
        case "error":
          NotificationManager.error("Error message", "Click me!", 5000, () => {
            alert("callback")
          })
          break
      }
    }
  }

  render() {
    return (
      <div>
         <button
          className="btn btn-info"
          onClick={this.createNotification("info")}
        >
          Info
        </button>
        {/*<hr />
        <button
          className="btn btn-success"
          onClick={this.createNotification("success")}
        >
          Success
        </button>
        <hr />
        <button
          className="btn btn-warning"
          onClick={this.createNotification("warning")}
        >
          Warning
        </button>
        <hr />
        <button
          className="btn btn-danger"
          onClick={this.createNotification("error")}
        >
          Error
        </button> */}

        {this.createNotification("sucess")}

        <NotificationContainer />
      </div>
    )
  }
}

export default Example

// import React from "react"
// import { NotificationContainer, NotificationManager } from "react-notifications"
// var msg = ""
// class Notification extends React.Component {
//   createNotification = (type) => {
//     return () => {
//       switch (type) {
//         case "info":
//           NotificationManager.info("hell")
//           break
//         case "success":
//           NotificationManager.success("Success message", msg)
//           break
//         case "warning":
//           NotificationManager.warning("hell", "Close after 3000ms", 3000)
//           break
//         case "error":
//           NotificationManager.error("Error message", "hell", 5000, () => {
//             alert("callback")
//           })
//           break
//       }
//     }
//   }

//   render() {
//     const { msg1, type } = this.props
//     msg = msg1
//     return (
//       //       <div>
//       //         <button onClick={this.createNotification({ type})}>
//       //           Click me
//       //         </button>
//       //         <button
//       //           className="btn btn-info"
//       //           onClick={this.createNotification("info")}
//       //         >
//       //           Info
//       //         </button>

//       //         <NotificationContainer />
//       //       </div>
//       <div>
//         <button
//           className="btn btn-info"
//           onClick={this.createNotification("info")}
//         >
//           Info
//         </button>
//         <hr />
//         <button
//           className="btn btn-success"
//           onClick={this.createNotification("success")}
//         >
//           Success
//         </button>
//         <hr />
//         <button
//           className="btn btn-warning"
//           onClick={this.createNotification("warning")}
//         >
//           Warning
//         </button>
//         <hr />
//         <button
//           className="btn btn-danger"
//           onClick={this.createNotification("error")}
//         >
//           Error
//         </button>

//         <NotificationContainer />
//       </div>
//     )
//     return null
//   }
// }

// export default Notification

// import React from "react"
// import ReactNotifications from "react-notifications-component"
// import { store } from "react-notifications-component"
// import "animate.css"

// import "react-notifications-component/dist.theme.css"
// import { Container } from "react-bootstrap"

// function App() {
//   return (
//     <div className="container">
//       <h1>ReactNotifications</h1>
//       <ReactNotifications></ReactNotifications>
//     </div>
//   )
// }

// function Home() {
//   const handle = () => {
//     store.addNotification({
//       content: Mynotify,
//       title: "New card added",
//       message: "hello",
//       type: "sucess",
//       Container: "top-right",
//       insert: "top",

//       animationIn: ["animated", "fadeIn"],
//       animationOut: ["animated", "fadeout"],
//       dismiss: {
//         duration: 2000,
//         showIcon: true
//       },
//       width: 600
//     })
//   }
//   return (
//     <div>
//       <button onClick={handle}>hello</button>
//     </div>
//   )
// }

// function Mynotify() {
//   return (
//     <div>
//       <h1>someMessage</h1>
//       <h1>Some message</h1>
//     </div>
//   )
// }
