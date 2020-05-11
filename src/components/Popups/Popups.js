// import React, { Component } from "react"
// import { Modal, Button } from "react-bootstrap"

// export class ModalComponent extends Component {
//   constructor(props) {
//     super(props)
//   }
//   render() {
//     return (
//       <Modal
//         {...this.props}
//         size="lg"
//         aria-labelledby="contained-modal-title-vcenter"
//         centered
//       >
//         <Modal.Header>
//           <Modal.Title id="contained-modal-title-vcenter">
//             Modal heading
//           </Modal.Title>
//         </Modal.Header>
//         <Modal.Body>
//           <h4>Centered Modal</h4>
//           <p>
//             Cras mattis consectetur purus sit amet fermentum. Cras justo odio,
//             dapibus ac facilisis in, egestas eget quam. Morbi leo risus, porta
//             ac consectetur ac, vestibulum at eros.
//           </p>
//         </Modal.Body>
//         <Modal.Footer>
//           <button onClick={this.props.onHide}>Close</button>
//         </Modal.Footer>
//       </Modal>
//     )
//   }
// }

// export default ModalComponent
// // class MyVerticallyCenteredModal extends Component {
// //   render() {
// //     console.log("Hello")
// //     const { onHide } = this.props
// //     return (
// //       <p>Hello world</p>
// //       // <Modal size="lg" aria-labelledby="contained-modal-title-vcenter" centered>
// //       //   <Modal.Header closeButton>
// //       //     <Modal.Title id="contained-modal-title-vcenter">
// //       //       Modal heading
// //       //     </Modal.Title>
// //       //   </Modal.Header>
// //       //   <Modal.Body>
// //       //     <h4>Centered Modal</h4>
// //       //     <p>
// //       //       Cras mattis consectetur purus sit amet fermentum. Cras justo odio,
// //       //       dapibus ac facilisis in, egestas eget quam. Morbi leo risus, porta
// //       //       ac consectetur ac, vestibulum at eros.
// //       //     </p>
// //       //   </Modal.Body>
// //       //   <Modal.Footer>
// //       //     <button onClick={onHide}>Close</button>
// //       //   </Modal.Footer>
// //       // </Modal>
// //     )
// //   }
// // }
// // // function App() {
// // //   const [modalShow, setModalShow] = React.useState(false)

// // //   return (
// // //     <>
// // //       <Button variant="primary" onClick={() => setModalShow(true)}>
// // //         Launch vertically centered modal
// // //       </Button>

// // // <MyVerticallyCenteredModal
// // //   show={modalShow}
// // //   onHide={() => setModalShow(false)}
// // // />
// // //     </>
// // //   )
// // // }

// // // render(<App />)

// // export default MyVerticallyCenteredModal







import React, { Component } from "react"
import ReactDOM from "react-dom"
import "./Popup.css"
import { Form } from "./Form"
import FocusTrap from "focus-trap-react"

// class ModalComponent extends Component{

//   render(){
//     const 


//   }
// }
export const Modal = ({
  onClickOutside,
  onKeyDown,
  modalRef,
  buttonRef,
  closeModal,
  onSubmit
}) => {
  return ReactDOM.createPortal(
    <FocusTrap>
      <aside
        tag="aside"
        role="dialog"
        tabIndex="-1"
        aria-modal="true"
        className="modal-cover"
        onClick={onClickOutside}
        onKeyDown={onKeyDown}
      >
        <div className="modal-area" ref={modalRef}>
          <button
            ref={buttonRef}
            aria-label="Close Modal"
            aria-labelledby="close-modal"
            className="_modal-close"
            onClick={closeModal}
          >
            <span id="close-modal" className="_hide-visual">
              Close
            </span>
            <svg className="_modal-close-icon" viewBox="0 0 40 40">
              <path d="M 10,10 L 30,30 M 30,10 L 10,30" />
            </svg>
          </button>
          <div className="modal-body">
            <Form onSubmit={onSubmit} />
          </div>
        </div>
      </aside>
    </FocusTrap>,
    document.body
  )
}

export default Modal
