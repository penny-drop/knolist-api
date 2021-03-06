import React, {useState} from "react";
import {Whisper, Tooltip, Input, Button} from "rsuite";
import makeHttpRequest from "../services/HttpRequest";

function ClusterTitle(props) {
    const [editing, setEditing] = useState(false);
    const [newTitle, setNewTitle] = useState("");
    const [cluster, setCluster] = useState(props.curClusterView);

    const styles = {
        position: 'absolute',
        top: 5,
        display: "flex",
        justifyContent: "center",
        width: "100%",
        fontSize: "1.5em"
    }

    let title = "";
    if (cluster !== null) title = cluster.name;

    const tooltip = (<Tooltip>Click to rename.</Tooltip>)

    const saveNewTitle = () => {
        const endpoint = "/clusters/" + cluster.id;
        const body = {"name": newTitle};
        makeHttpRequest(endpoint, "PATCH", body).then((res) => {
            props.setCurClusterView(res.body.cluster);
            setEditing(false);
            setCluster(res.body.cluster);
        });
    }

    if (cluster === null) return null;
    if (!editing) return (
        <Whisper placement="bottom" trigger="hover" speaker={tooltip}>
            <div style={styles} onClick={() => setEditing(true)}>{title}</div>
        </Whisper>
    );
    return (
        <div style={styles}>
            <Input style={{width: 120}} defaultValue={title} autoFocus
                   onBlur={() => setEditing(false)}
                   onInput={e => setNewTitle(e.target.value)}/>
            <Button size="xs" style={{marginLeft: 5}} onMouseDown={e => e.preventDefault()}
                    onClick={() => saveNewTitle()}>Save</Button>
        </div>
    );
}

export default ClusterTitle;