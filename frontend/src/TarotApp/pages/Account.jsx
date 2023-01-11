import { Row, Col, Container } from "react-bootstrap";
import ProfileSection from "../components/ProfileSection";
import "./Account.css";

export default function Account() {
  return (
    <Container id="account" className="square border">
      <div className="container">
        <Row className="square border-bottom">
          <ProfileSection />
        </Row>
      </div>
    </Container>
  );
}
