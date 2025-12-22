CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    path TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    algorithm VARCHAR(100),
    dataset_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE experiments (
    id SERIAL PRIMARY KEY,
    model_id INT,
    metric_name VARCHAR(50),
    metric_value FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE deployments (
    id SERIAL PRIMARY KEY,
    model_id INT,
    endpoint TEXT,
    type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
