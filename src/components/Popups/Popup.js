import React, { Component } from "react"
import { Modal, Button, Row, Col, Form } from "react-bootstrap"

export class ModalComponent extends Component {
  constructor(props) {
    super(props)
  }
  render() {
    // console.log(this.props.onHide)
    return (
      <Modal
        {...this.props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            Message from the server!!!
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={this.props.handleSubmitStartRun}>
            <Form.Group controlId="formBasicEmail">
              <Form.Label>
                <h3>{this.props.promptMessage}</h3>
              </Form.Label>
              <Form.Control
                type="text"
                placeholder={this.props.promptMessage}
                name="inputItems1"
                onChange={this.props.handleChange}
              />
              <Form.Text className="text-muted">
                Please provide proper format for the input
              </Form.Text>
            </Form.Group>

            <Form.Group controlId="formBasicPassword">
              <Form.Label>
                <h3>Confirm</h3>
              </Form.Label>
              <Form.Control
                type="text"
                placeholder="Confirm"
                name="inputItems2"
                onChange={this.props.handleChange}
              />
            </Form.Group>
            <Form.Group controlId="formBasicCheckbox"></Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button type="submit" onClick={this.props.handleSubmitStartRun}>
            Submit
          </Button>
        </Modal.Footer>
      </Modal>
    )
  }
}



export default ModalComponent
