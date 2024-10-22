CREATE TABLE usuario (
    id VARCHAR(64) PRIMARY KEY,
    id_mensagem INT NOT NULL,
    pergunta TEXT,
    resposta TEXT
);

CREATE TABLE notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_user INT,
    nota INT CHECK (nota >= 1 AND nota <= 5),
    FOREIGN KEY (id_user) REFERENCES usuario(id)
);
