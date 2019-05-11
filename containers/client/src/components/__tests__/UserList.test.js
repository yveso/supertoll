import React from "react";
import { shallow } from "enzyme";
import renderer from "react-test-renderer";

import UsersList from "../UsersList";

const users = [
  { active: true, email: "max@maxundmoritz.de", id: 0, username: "Max" },
  { active: true, email: "moritz@maxundmoritz.de", id: 0, username: "Moritz" },
];

test("UsersList renders", () => {
  const wrapper = shallow(<UsersList users={users} />);
  const element = wrapper.find("li");
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe("Max");
});

test("UsersList renders snapshot", () => {
  const tree = renderer.create(<UsersList users={users} />).toJSON();
  expect(tree).toMatchSnapshot();
});
