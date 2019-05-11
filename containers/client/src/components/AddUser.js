import React from "react";

function AddUser(props) {
  const [username, setUsername] = React.useState("");
  const [email, setEmail] = React.useState("");

  function handleChange(e) {
    const { name, value } = e.target;
    if (name === "username") {
      setUsername(value);
    } else if (name === "email") {
      setEmail(value);
    }
  }

  function addUser(event) {
    event.preventDefault();
    const data = {
      username: username,
      email: email,
    };
    fetch(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then(_ => {
        props.refresh();
        setUsername("");
        setEmail("");
      })
      .catch(error => console.log(error));
  }
  return (
    <form onSubmit={event => addUser(event)}>
      <div>
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={username}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <input
          type="text"
          name="email"
          placeholder="Email"
          value={email}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <input type="submit" value="Submit" />
      </div>
    </form>
  );
}

export default AddUser;
