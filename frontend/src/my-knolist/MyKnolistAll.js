import React from "react";

function MyKnolistAll() {
  return (
    <div>
      <p className="myknolist-main-subtitle" style={{ marginTop: "7vh" }}>All</p>
      <div className="myknolist-container" style={{ marginTop: "3vh" }}>
        <div className="myknolist-all-list-info">
          Name
        </div>
        <div className="myknolist-all-list-info">
          Last Modified
        </div>
      </div>
    </div>
  );
}

export default MyKnolistAll;