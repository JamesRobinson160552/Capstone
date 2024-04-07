import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const Quandary());
}

class Quandary extends StatelessWidget {
  const Quandary({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Quandary',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const WelcomePage(),
        '/main': (context) => const MainPage(),
      },
    );
  }
}

class WelcomePage extends StatelessWidget {
  const WelcomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              const Text(
                'Welcome to Quandary!',
                style: TextStyle(fontSize: 24),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 20),
              const Text(
                'Got a difficult situation? Unsure if you acted right? Tell Quandary in 250 characters or more and get an answer!',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 16),
              ),
              const SizedBox(height: 40),
              ElevatedButton(
                onPressed: () {
                  Navigator.pushNamed(context, '/main');
                },
                child: const Text('Enter'),
              ),
              const SizedBox(height: 20),
              const Text(
                'Prepared by James Robinson for COMP 4983, Winter 2024 \nSupervisor Dr. Greg Lee\nAcadia Univerity\n\nQuandary is an experimental tool and should not be used to influence any important decisions and is not an accurate determinant of legality or morality.',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 16),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  final TextEditingController _textController = TextEditingController();
  String _outputText = '';
  final String _baseUrl = 'https://jamesrobinson.pythonanywhere.com';

  void _submitText() async {
    if (_textController.text.length < 250) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Input must be at least 250 characters.')),
      );
      return;
    }

    try {
      final response = await http.get(
        Uri.parse('$_baseUrl?input=${_textController.text}'),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data['prediction'] == '0') {
          setState(() {
            _outputText = 'NTA: You\'re probably okay! Based on Quandary\'s prediction, you acted correctly in this situation. Good job!';
          });
        } else {
          setState(() {
            _outputText = 'YTA: Seems like you maybe made a mistake here. Based on Quandary\'s prediction, you probably want to reflect on how other people might feel.';
          });
        }
      } else {
        throw Exception('Failed to load data');
      }
    } catch (e) {
      //print('Error: $e');
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Failed to connect to the server.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Quandary'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            SingleChildScrollView(
              scrollDirection: Axis.vertical,
              physics: const AlwaysScrollableScrollPhysics(),
              child: ConstrainedBox(
                constraints: BoxConstraints(
                  maxHeight: MediaQuery.of(context).size.height * 0.8,
                ),
                child: TextField(
                  controller: _textController,
                  maxLines: null,
                  keyboardType: TextInputType.multiline,
                  decoration: const InputDecoration(
                    hintText: 'Enter your text here',
                    border: OutlineInputBorder(),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 2),
            ElevatedButton(
              onPressed: _submitText,
              child: const Text('Submit'),
            ),
            const SizedBox(height: 20),
            Text(
              _outputText,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 20),
            ),
          ],
        ),
      ),
    );
  }
}

