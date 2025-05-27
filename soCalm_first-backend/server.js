const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const bodyParser = require('body-parser');
const User = require('./models/User');

const app = express();
app.use(cors());
app.use(bodyParser.json());

mongoose.connect('mongodb://localhost:27017/socalmDB', {
    useNewUrlParser: true,
    useUnifiedTopology: true
});

app.post('/signup', async (req, res) => {
    const { fullName, username, password } = req.body;
    try {
        const user = new User({ fullName, username, password });
        await user.save();
        res.json({ success: true });
    } catch (err) {
        res.json({ success: false, message: err.message });
    }
});

app.listen(3000, () => console.log('백엔드 서버 실행 중: http://localhost:3000'));
