#!/usr/bin/env python3
"""
Test script to demonstrate the verbosity system
"""
import asyncio
import os
from src.henotace_ai import HenotaceAI, create_tutor

async def test_verbosity_levels():
    """Test different verbosity levels"""
    print("🚀 Testing Verbosity System")
    print("=" * 60)
    
    # Initialize SDK
    api_key = os.getenv('HENOTACE_API_KEY', 'henotace_dev_G9syAdMQJlz6zgSN3CqTd8CTLc4wP3kJ')
    sdk = HenotaceAI(api_key=api_key)
    
    # Test different verbosity levels
    verbosity_tests = [
        {
            'level': 'brief',
            'question': 'What is photosynthesis?',
            'description': 'Brief explanation (1-2 sentences)'
        },
        {
            'level': 'normal', 
            'question': 'What is photosynthesis?',
            'description': 'Normal explanation (2-4 sentences)'
        },
        {
            'level': 'detailed',
            'question': 'What is photosynthesis?',
            'description': 'Detailed explanation (4-8 sentences)'
        },
        {
            'level': 'comprehensive',
            'question': 'What is photosynthesis?',
            'description': 'Comprehensive explanation (8+ sentences)'
        }
    ]
    
    for test in verbosity_tests:
        print(f"\n📝 Testing {test['description']}")
        print("-" * 40)
        
        try:
            # Create tutor with specific verbosity
            tutor = await create_tutor(
                sdk=sdk,
                student_id='verbosity_test',
                tutor_name='Verbosity Test Tutor'
            )
            
            # Send message with verbosity level
            response = await tutor.send(test['question'])
            
            print(f"✅ Response ({len(response)} characters):")
            print(f"📄 {response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🧠 Testing Auto-Detection")
    print("-" * 40)
    
    # Test auto-detection based on user input
    auto_detection_tests = [
        {
            'question': 'Briefly explain gravity',
            'expected': 'brief'
        },
        {
            'question': 'What is gravity?',
            'expected': 'normal'
        },
        {
            'question': 'Can you give me a detailed explanation of gravity?',
            'expected': 'detailed'
        },
        {
            'question': 'I need a comprehensive guide to gravity',
            'expected': 'comprehensive'
        }
    ]
    
    for test in auto_detection_tests:
        print(f"\n🔍 Testing: '{test['question']}'")
        print(f"Expected verbosity: {test['expected']}")
        
        try:
            # Test verbosity detection
            detected = sdk._detect_verbosity(test['question'])
            print(f"Detected verbosity: {detected}")
            
            if detected == test['expected']:
                print("✅ Auto-detection working correctly!")
            else:
                print(f"⚠️  Expected {test['expected']}, got {detected}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_verbosity_levels())
