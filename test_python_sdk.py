#!/usr/bin/env python3
"""
Test script for Python SDK with verbosity system
"""
import asyncio
import os
from src.henotace_ai import HenotaceAI, create_tutor

async def test_python_sdk():
    """Test Python SDK with different verbosity levels"""
    print("🚀 Testing Python SDK")
    print("=" * 60)
    
    # Initialize SDK
    api_key = os.getenv('HENOTACE_API_KEY', 'henotace_dev_G9syAdMQJlz6zgSN3CqTd8CTLc4wP3kJ')
    sdk = HenotaceAI(api_key=api_key)
    
    print("📡 Checking API status...")
    try:
        status = sdk.get_status()
        print(f"✅ API Status: {status}")
    except Exception as e:
        print(f"❌ Status Error: {e}")
        return
    
    print("\n👨‍🏫 Creating tutor...")
    try:
        tutor = await create_tutor(
            sdk=sdk,
            student_id='test_student',
            tutor_name='Test Tutor'
        )
        print(f"✅ Tutor created: {tutor.ids}")
    except Exception as e:
        print(f"❌ Error creating tutor: {e}")
        return
    
    # Test different verbosity levels
    test_questions = [
        {
            'question': 'What is a chemical equation?',
            'description': 'Normal question'
        },
        {
            'question': 'Briefly explain photosynthesis',
            'description': 'Brief request'
        },
        {
            'question': 'Can you give me a detailed explanation of gravity?',
            'description': 'Detailed request'
        },
        {
            'question': 'I need a comprehensive guide to thermodynamics',
            'description': 'Comprehensive request'
        }
    ]
    
    for i, test in enumerate(test_questions, 1):
        print(f"\n📝 Test {i}: {test['description']}")
        print("-" * 40)
        print(f"Question: {test['question']}")
        
        try:
            response = await tutor.send(test['question'])
            print(f"✅ Response ({len(response)} characters):")
            print(f"📄 {response}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_python_sdk())
