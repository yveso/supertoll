import React from "react";
import UsersList from "./components/UsersList";
import AddUser from "./components/AddUser";

function App() {
  const [users, setUsers] = React.useState([]);
  React.useEffect(() => {
    getUsers();
  }, []);

  function getUsers() {
    fetch(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
      .then(response => response.json())
      .then(result => setUsers(result.data.users))
      .catch(error => console.log(error));
  }

  return (
    <>
      <h1>All Users</h1>
      <br />
      <AddUser refresh={getUsers} />
      <br />
      <UsersList users={users} />
    </>
  );
}

export default App;
