import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';

interface CardGridElementProps {
    element: {
      name: string;
      values: { key: string; value: string }[];
    };
  }
  
  const CardGridElement: React.FC<CardGridElementProps> = ({ element }) => {
    const { name, values } = element;
    return (
        <Card>
            <Card.Body>
            <Card.Title>{name}</Card.Title>
            <ListGroup variant="flush">
                {values.map((item, index) => (
                <ListGroup.Item key={index}>
                    {item.key}: {item.value}
                </ListGroup.Item>
                ))}
            </ListGroup>
            </Card.Body>
        </Card>
        );
    
}

export default CardGridElement;