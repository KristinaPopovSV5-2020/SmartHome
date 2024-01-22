import '../css/Index.css';

import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import CardGridElement from './CardGridElement';

const CardGrid: React.FC = () => {
  const data = [
    {
      name: 'Element 1',
      values: [
        { key: 'Key1', value: 'Value1' },
        { key: 'Key2', value: 'Value2' },
      ],
    },
    {
      name: 'Element 2',
      values: [
        { key: 'Key1', value: 'Value1' },
        { key: 'Key2', value: 'Value2' },
      ],
    }
  ];

  return (
    <div className="card-grid-container">
      <Row xs={6} md={4} className="g-24">
        {data.map((element, idx) => (
          <Col key={idx}>
            <CardGridElement element={element} />
          </Col>
        ))}
      </Row>
    </div>
  );
}

export default CardGrid;