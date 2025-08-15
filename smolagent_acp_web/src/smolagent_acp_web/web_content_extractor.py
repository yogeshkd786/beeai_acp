"""
Web Content Extractor for Health Information
Enhanced content extraction and processing for health-related web content.
"""

import logging
import re
from typing import List, Dict, Optional
import trafilatura

logger = logging.getLogger(__name__)

class HealthContentExtractor:
    """
    Enhanced content extractor specifically designed for health information.
    """
    
    def __init__(self):
        """Initialize the health content extractor."""
        self.trusted_health_sources = [
            'mayoclinic.org', 'webmd.com', 'healthline.com', 'medlineplus.gov',
            'nih.gov', 'cdc.gov', 'who.int', 'nhs.uk', 'clevelandclinic.org',
            'hopkinsmedicine.org', 'health.harvard.edu', 'uptodate.com'
        ]
        
        self.medical_disclaimers = [
            "This information is for educational purposes only",
            "Consult your healthcare provider",
            "Not intended to replace professional medical advice",
            "Seek immediate medical attention for emergencies"
        ]
    
    def get_website_text_content(self, url: str) -> str:
        """
        Extract text content from a website URL using trafilatura.
        
        This function takes a url and returns the main text content of the website.
        The text content is extracted using trafilatura and easier to understand.
        The results are better for human or LLM consumption than raw HTML.
        
        Args:
            url: The URL to extract content from
            
        Returns:
            str: Extracted text content from the website
        """
        try:
            # Send a request to the website
            downloaded = trafilatura.fetch_url(url)
            if downloaded is None:
                logger.warning(f"Failed to download content from {url}")
                return f"Unable to access content from {url}"
            
            # Extract text content
            text = trafilatura.extract(downloaded)
            if text is None:
                logger.warning(f"Failed to extract text from {url}")
                return f"Unable to extract readable content from {url}"
            
            # Enhance for health content
            enhanced_text = self._enhance_health_content(text, url)
            
            logger.info(f"Successfully extracted {len(enhanced_text)} characters from {url}")
            return enhanced_text
            
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return f"Error accessing {url}: {str(e)}"
    
    def _enhance_health_content(self, content: str, url: str) -> str:
        """
        Enhance extracted health content with additional context and validation.
        
        Args:
            content: Raw extracted content
            url: Source URL
            
        Returns:
            str: Enhanced content with health-specific formatting
        """
        # Add source information
        source_info = f"\n\n📄 Source: {url}\n"
        
        # Check if source is trusted
        is_trusted = any(domain in url for domain in self.trusted_health_sources)
        if is_trusted:
            source_info += "✅ This is a trusted medical source.\n"
        else:
            source_info += "⚠️ Please verify this information with trusted medical sources.\n"
        
        # Clean up content
        cleaned_content = self._clean_health_content(content)
        
        return cleaned_content + source_info
    
    def _clean_health_content(self, content: str) -> str:
        """
        Clean and format health content for better readability.
        
        Args:
            content: Raw content to clean
            
        Returns:
            str: Cleaned and formatted content
        """
        # Remove excessive whitespace
        content = re.sub(r'\n\s*\n', '\n\n', content)
        content = re.sub(r' +', ' ', content)
        
        # Remove common web artifacts
        content = re.sub(r'Cookie Policy|Privacy Policy|Terms of Service', '', content, flags=re.IGNORECASE)
        content = re.sub(r'Advertisement|Skip to main content', '', content, flags=re.IGNORECASE)
        
        # Highlight important medical information
        content = re.sub(r'(IMPORTANT|WARNING|CAUTION):', r'⚠️ \1:', content, flags=re.IGNORECASE)
        content = re.sub(r'(NOTE|REMEMBER):', r'📝 \1:', content, flags=re.IGNORECASE)
        
        return content.strip()
    
    def enhance_health_response(self, response: str) -> str:
        """
        Enhance agent response with health-specific formatting and disclaimers.
        
        Args:
            response: Raw agent response
            
        Returns:
            str: Enhanced response with health disclaimers and formatting
        """
        # Add medical disclaimer if not present
        has_disclaimer = any(disclaimer.lower() in response.lower() for disclaimer in self.medical_disclaimers)
        
        if not has_disclaimer:
            medical_disclaimer = """

⚕️ IMPORTANT MEDICAL DISCLAIMER:
This information is for educational purposes only and should not replace professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read here.

🚨 For medical emergencies, call 911 or contact your local emergency services immediately.
"""
            response += medical_disclaimer
        
        # Format the response for better readability
        response = self._format_health_response(response)
        
        return response
    
    def _format_health_response(self, response: str) -> str:
        """
        Format health response with appropriate sections and emphasis.
        
        Args:
            response: Response to format
            
        Returns:
            str: Formatted response
        """
        # Add section headers for common health topics
        response = re.sub(r'(Symptoms?:)', r'🔍 \1', response, flags=re.IGNORECASE)
        response = re.sub(r'(Treatment?s?:)', r'💊 \1', response, flags=re.IGNORECASE)
        response = re.sub(r'(Causes?:)', r'🧬 \1', response, flags=re.IGNORECASE)
        response = re.sub(r'(Prevention:)', r'🛡️ \1', response, flags=re.IGNORECASE)
        response = re.sub(r'(Diagnosis:)', r'🔬 \1', response, flags=re.IGNORECASE)
        
        # Emphasize when to see a doctor
        response = re.sub(
            r'(see a doctor|consult a physician|seek medical attention)',
            r'👨‍⚕️ \1',
            response,
            flags=re.IGNORECASE
        )
        
        return response
    
    def validate_health_source(self, url: str) -> Dict[str, any]:
        """
        Validate if a health source is trustworthy.
        
        Args:
            url: URL to validate
            
        Returns:
            Dict: Validation results with trust score and reasoning
        """
        validation_result = {
            'is_trusted': False,
            'trust_score': 0,
            'reasoning': [],
            'source_type': 'unknown'
        }
        
        # Check against trusted sources
        for trusted_domain in self.trusted_health_sources:
            if trusted_domain in url:
                validation_result['is_trusted'] = True
                validation_result['trust_score'] = 10
                validation_result['reasoning'].append(f"Recognized trusted medical source: {trusted_domain}")
                
                # Determine source type
                if any(term in trusted_domain for term in ['gov', 'nih', 'cdc']):
                    validation_result['source_type'] = 'government'
                elif any(term in trusted_domain for term in ['clinic', 'hospital', 'harvard', 'hopkins']):
                    validation_result['source_type'] = 'medical_institution'
                else:
                    validation_result['source_type'] = 'health_website'
                break
        
        # Additional validation criteria
        if '.edu' in url:
            validation_result['trust_score'] += 3
            validation_result['reasoning'].append("Educational institution domain")
        
        if 'peer-reviewed' in url or 'pubmed' in url:
            validation_result['trust_score'] += 5
            validation_result['reasoning'].append("Appears to be peer-reviewed content")
        
        # Set trust threshold
        if validation_result['trust_score'] >= 7:
            validation_result['is_trusted'] = True
        
        return validation_result
    
    def extract_health_facts(self, content: str) -> List[str]:
        """
        Extract key health facts from content.
        
        Args:
            content: Health content to analyze
            
        Returns:
            List[str]: List of extracted health facts
        """
        facts = []
        
        # Look for common health fact patterns
        fact_patterns = [
            r'Studies show that ([^.]+\.)',
            r'Research indicates ([^.]+\.)',
            r'According to the ([^,]+), ([^.]+\.)',
            r'The ([^,]+) recommends ([^.]+\.)',
            r'([0-9]+%?) of (people|patients|adults|children) ([^.]+\.)'
        ]
        
        for pattern in fact_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    fact = ' '.join(match)
                else:
                    fact = match
                facts.append(fact.strip())
        
        return facts[:10]  # Limit to top 10 facts
