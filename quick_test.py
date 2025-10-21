#!/usr/bin/env python3
"""
Quick test script to demonstrate the updated Python SDK functionality
"""

import asyncio
import os
from henotace_ai import HenotaceAI, create_tutor, SessionSubject, InMemoryConnector

async def main():
    # Use the provided API key
    api_key = "henotace_dev_WiYGGqY1LnXWJiDGfDi0cXHk27mlOBII"
    
    print("🚀 Henotace AI Python SDK v1.2.0 - Quick Test")
    print("=" * 50)
    
    # Initialize SDK
    sdk = HenotaceAI(api_key=api_key)
    
    print("✅ SDK initialized with Bearer token authentication")
    
    # Test basic chat completion
    print("\n💬 Testing basic chat completion...")
    try:
        response = sdk.complete_chat(
            history=[{'role': 'user', 'content': 'Hello'}],
            input_text='Explain algebra briefly',
            subject='mathematics',
            topic='algebra'
        )
        print(f"✅ Chat completion works: {len(response.get('ai_response', ''))} characters")
    except Exception as e:
        print(f"❌ Chat completion failed: {e}")
        return
    
    # Test classwork generation
    print("\n📝 Testing classwork generation...")
    try:
        classwork = sdk.generate_classwork(
            history=[
                {'role': 'user', 'content': 'I need help with linear equations'},
                {'role': 'assistant', 'content': 'Linear equations are equations where the highest power is 1. For example, 2x + 3 = 7.'}
            ],
            subject='mathematics',
            topic='linear equations',
            question_count=3,
            difficulty='medium'
        )
        questions = classwork.get('questions', [])
        print(f"✅ Classwork generation works: {len(questions)} questions generated")
        
        if questions:
            print("\n📋 Sample question:")
            print(f"   {questions[0].get('question', 'No question text')}")
    except Exception as e:
        print(f"❌ Classwork generation failed: {e}")
        return
    
    # Test tutor-based functionality
    print("\n👨‍🏫 Testing tutor-based functionality...")
    try:
        tutor = await create_tutor(
            sdk=sdk,
            student_id="test_student",
            tutor_name="Math Tutor",
            subject=SessionSubject(id="math", name="Mathematics", topic="Algebra")
        )
        
        # Send a message
        response = await tutor.send("Can you help me solve 2x + 5 = 13?")
        print(f"✅ Tutor chat works: {len(response)} characters")
        
        # Generate classwork from conversation
        classwork = await tutor.generate_classwork(question_count=2, difficulty='easy')
        questions = classwork.get('questions', [])
        print(f"✅ Tutor classwork generation works: {len(questions)} questions")
        
    except Exception as e:
        print(f"❌ Tutor functionality failed: {e}")
        return
    
    print("\n🎉 All tests passed! Python SDK v1.2.0 is working correctly!")
    print("\n📚 New Features Added:")
    print("   ✅ Classwork generation functionality")
    print("   ✅ Bearer token authentication")
    print("   ✅ Enhanced error handling")
    print("   ✅ Comprehensive examples and documentation")
    print("   ✅ Integration tests")

if __name__ == "__main__":
    asyncio.run(main())
