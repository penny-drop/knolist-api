import React, { useState } from "react";
import { Modal, Button, Form, FormGroup, ControlLabel, HelpBlock, FormControl, Alert } from "rsuite";
import makeHttpRequest from "../services/HttpRequest";
import { useHistory } from "react-router-dom";

function NewProjectModal(props) {
    const show = props.show;
    const setShow = props.setShow;
    const history = useHistory();
    const [loading, setLoading] = useState(false);

    const openProject = () => {
        const projectTitle = document.getElementById("titleInput").value;
        let projectDesc = document.getElementById("descriptionInput").value;
        if (projectTitle.length === 0) {
            setLoading(false);
            Alert.error("Title is required!", 2000);
            return;
        }
        let body = {};
        if (projectDesc == null || projectDesc === "") {
            body = {
                "title": projectTitle
            }
        } else {
            body = {
                "title": projectTitle,
                "description": projectDesc
            }
        }
        makeHttpRequest("/projects", "POST", body).then(response => {
            localStorage.setItem(process.env.REACT_APP_LOCAL_STORAGE_CUR_PROJECT, JSON.stringify(response.body.project));
            setShow(false);
            if (props.fromSidebar) history.go(0);
            else history.push("/");
        });
    }

    const cancel = () => props.noCancel ? Alert.error("Please create a project!") : setShow(false);

    return (
        <Modal show={show} style={{ overflow: "hidden" }} onHide={cancel}>
            <Modal.Header><Modal.Title>New Project</Modal.Title></Modal.Header>
            <Modal.Body>
                <Form fluid>
                    <FormGroup controlId="titleInput">
                        <ControlLabel>Title</ControlLabel>
                        <FormControl name="title" />
                        <HelpBlock>Required</HelpBlock>
                    </FormGroup>
                    <FormGroup controlId="descriptionInput">
                        <ControlLabel>Description</ControlLabel>
                        <FormControl
                            rows={5}
                            name="description"
                            componentClass="textarea" />
                    </FormGroup>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                    <Button
                        onClick={() => {
                            setLoading(true);
                            openProject();
                        }}
                        appearance="primary"
                        loading={loading}>
                        Create
                    </Button>
                <Button onClick={cancel} appearance="default">
                    Cancel
                </Button>
            </Modal.Footer>
        </Modal>
    );
}

export default NewProjectModal;