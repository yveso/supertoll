import React from "react";

function UsersList({ users }) {
  return (
    <ol>
      {users.map((user, index) => (
        <li key={index}>{user.username}</li>
      ))}
    </ol>
  );
}

export default UsersList;
