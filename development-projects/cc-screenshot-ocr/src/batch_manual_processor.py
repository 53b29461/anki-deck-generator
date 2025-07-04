#!/usr/bin/env python3
"""
101問の手動処理を効率化するバッチシステム
"""

import sys
sys.path.append('/home/user/.pg/development-projects/cc-screenshot-ocr/src')

from manual_anki_cards import ManualAnkiCardGenerator

def create_all_cards():
    generator = ManualAnkiCardGenerator()
    
    # 問題データを順番に入力
    questions = [
        {
            'number': 1,
            'situation': "Steve is a security practitioner assigned to come up with a protective measure for ensuring that cars don't collide with pedestrians.",
            'question': "What is probably the most effective type of control for this task?",
            'choices': ["Administrative", "Nuanced", "Physical", "Technical"],
            'correct': "Physical",
            'explanation': "Physical controls, such as fences, walls and bollards, will be most likely to ensure cars cannot collide with pedestrians by creating actual barriers between cars and pedestrians."
        },
        {
            'number': 2,
            'situation': "Chad is a security practitioner tasked with ensuring that the information on the organization's public website is not changed by anyone outside the organization.",
            'question': "Which concept does this task demonstrate?",
            'choices': ["Availability", "Confidentiality", "Confirmation", "Integrity"],
            'correct': "Integrity",
            'explanation': "Preventing unauthorized modification is the definition of integrity."
        },
        {
            'number': 3,
            'situation': "",  # 状況説明なし
            'question': "Which of the following is an example of a 'Something you know' authentication factor?",
            'choices': ["Fingerprint", "Iris scan", "Password", "User ID"],
            'correct': "Password",
            'explanation': "A password is something the user knows and can present as an authentication factor to confirm an identity assertion."
        },
        {
            'number': 4,
            'situation': "",
            'question': "Which of the following is an example of a 'Something you are' authentication factor?",
            'choices': ["A credit card presented to a cash machine", "A photograph of your face", "A user ID", "Your password and PIN"],
            'correct': "A photograph of your face",
            'explanation': "A facial photograph is something you are, your appearance."
        },
        {
            'number': 5,
            'situation': "A system collects transactional information and stores it in a record in order to show which users performed which actions.",
            'question': "Which concept does this demonstrate?",
            'choices': ["Biometrics", "Multifactor authentication", "Non-repudiation", "Privacy"],
            'correct': "Non-repudiation",
            'explanation': "Non-repudiation describes the concept that users cannot deny having performed transactions that they did, in fact, conduct. A system that keeps a record of user transactions provides non-repudiation."
        },
        {
            'number': 6,
            'situation': "",
            'question': "What is the European Union (EU) law that grants legal protections to individual human privacy?",
            'choices': ["The General Data Protection Regulation", "The Maastricht Treaty (the Treaty on European Union)", "The Privacy Human Rights Act", "The Schengen Agreement"],
            'correct': "The General Data Protection Regulation",
            'explanation': "The GDPR is the EU law that treats privacy as a human right."
        },
        {
            'number': 7,
            'situation': "",
            'question': "For which of the following systems would the security concept of availability be considered MOST important?",
            'choices': ["Medical systems that monitor patient conditions in an intensive-care unit", "Medical systems that store patient data", "Online streaming of camera feeds that display historical works of art in museums around the world", "Retail records of past transactions"],
            'correct': "Medical systems that monitor patient conditions in an intensive-care unit",
            'explanation': "Information that reflects patient conditions is data that necessarily must be kept available in real time, because that data is directly linked to patient well-being (and possibly a matter of life or death). This is, by far, the most important of the options listed."
        },
        {
            'number': 8,
            'situation': "",
            'question': "For which of the following assets is integrity probably the MOST important security aspect?",
            'choices': ["One frame of a streaming video", "Software that checks the spelling of product descriptions for a retail website", "The color scheme of a marketing website", "The file that contains passwords used to authenticate users"],
            'correct': "The file that contains passwords used to authenticate users",
            'explanation': "If a password file is modified, the impact to the environment could be significant; there is a possibility that all authorized users could be denied access, or that anyone (including unauthorized users) could be granted access. The integrity of the password file is probably the most crucial of the four options listed."
        },
        {
            'number': 9,
            'situation': "",
            'question': "In risk management, which concept reflects something a security practitioner might need to protect?",
            'choices': ["Asset", "Likelihood", "Threat", "Vulnerability"],
            'correct': "Asset",
            'explanation': "An asset is anything with value, and a security practitioner may need to protect assets."
        },
        {
            'number': 10,
            'situation': "",
            'question': "In risk management concepts, what is something or someone that poses risk to an organization or asset?",
            'choices': ["Asset", "Control", "Fear", "Threat"],
            'correct': "Threat",
            'explanation': "A threat is something or someone that poses risk to the organization; this is the definition of a threat."
        },
        {
            'number': 11,
            'situation': "",
            'question': "Of the following, which would probably NOT be considered a threat?",
            'choices': ["A laptop with sensitive data on it", "An external attacker trying to gain unauthorized access to the environment", "Natural disaster", "Unintentional damage to the system caused by a user"],
            'correct': "A laptop with sensitive data on it",
            'explanation': "A laptop, and the data on it, are assets, not threats. All the other answers are examples of threats because they all have the potential to cause adverse impact to the organization and its assets."
        },
        {
            'number': 12,
            'situation': "",
            'question': "Which of the following probably poses the MOST risk?",
            'choices': ["A high-likelihood, high-impact event", "A high-likelihood, low-impact event", "A low-likelihood, high-impact event", "A low-likelihood, low-impact event"],
            'correct': "A high-likelihood, high-impact event",
            'explanation': "An event that has a significant probability of occurring ('high-likelihood') and also has a severe negative consequence (high-impact) poses the most risk."
        },
        {
            'number': 13,
            'situation': "",
            'question': "Within the organization, who can identify risk?",
            'choices': ["Anyone", "Any security team member", "Senior management", "The security manager"],
            'correct': "Anyone",
            'explanation': "Anyone within the organization can identify risk."
        },
        {
            'number': 14,
            'situation': "Kerpak works in the security office of a medium-sized entertainment company. Kerpak is asked to assess a particular threat, and he suggests that the best way to counter this threat would be to purchase and implement a particular security solution.",
            'question': "What concept does Kerpak's solution demonstrate?",
            'choices': ["Acceptance", "Avoidance", "Mitigation", "Transference"],
            'correct': "Mitigation",
            'explanation': "Applying a security solution (a type of control) is an example of mitigation."
        },
        {
            'number': 15,
            'situation': "Sophia is visiting Las Vegas and decides to put a bet on a particular number on a roulette wheel.",
            'question': "Fill in the missing word: This is an example of _______.",
            'choices': ["Acceptance", "Avoidance", "Mitigation", "Transference"],
            'correct': "Acceptance",
            'explanation': "Sophia is accepting the risk that the money will be lost, even though the likelihood is high; Sophia has decided that the potential benefit (winning the bet), while low in likelihood, is worth the risk."
        },
        {
            'number': 16,
            'situation': "Phrenal is selling a used laptop in an online auction. Phrenal has estimated the value of the laptop to be $100, but has seen other laptops of similar type and quality sell for both more and less than that amount. Phrenal hopes that the laptop will sell for $100 or more, but is prepared to take less for it if nobody bids that amount.",
            'question': "What concept does this demonstrate?",
            'choices': ["Risk inversion", "Risk tolerance", "Threat", "Vulnerability"],
            'correct': "Risk tolerance",
            'explanation': "Phrenal has decided there is an acceptable level of risk associated with the online sale of the laptop; this is within Phrenal's risk tolerance."
        },
        {
            'number': 17,
            'situation': "A software firewall is an application that runs on a device and prevents specific types of traffic from entering that device.",
            'question': "Which type of control is this?",
            'choices': ["Administrative", "Passive", "Physical", "Technical"],
            'correct': "Technical",
            'explanation': "A software firewall is a technical control because it is a part of the IT environment."
        },
        {
            'number': 18,
            'situation': "At the airport, there are red lines painted on the ground next to the runway, which prohibits traffic from crossing it.",
            'question': "Which type of control does this exemplify?",
            'choices': ["Administrative", "Critical", "Physical", "Technical"],
            'correct': "Physical",
            'explanation': "A red line that is painted on the ground at the airport to prohibit traffic from crossing it is a physical control, like a stop sign on the roadway is."
        },
        {
            'number': 19,
            'situation': "A bollard is a post set securely in the ground in order to prevent a vehicle from entering an area or driving past a certain point.",
            'question': "Bollards are an example of which type of control?",
            'choices': ["Administrative", "Critical", "Physical", "Technical"],
            'correct': "Physical",
            'explanation': "A bollard is a tangible object that prevents a physical act from occurring; this is a physical control."
        },
        {
            'number': 20,
            'situation': "Druna is a security practitioner tasked with ensuring that laptops are not stolen from the organization's offices.",
            'question': "Which kind of security control would probably be BEST for this purpose?",
            'choices': ["Administrative", "Obverse", "Physical", "Technical"],
            'correct': "Physical",
            'explanation': "Because laptops are tangible objects, and Druna is trying to ensure that these objects are not moved from a certain place, physical controls are probably best for the purpose."
        },
        {
            'number': 21,
            'situation': "Triffid Corporation has a policy that all employees must receive security awareness instruction before using email; the company wants to make employees aware of potential phishing attempts that the employees might receive via email.",
            'question': "What kind of control is this instruction?",
            'choices': ["Administrative", "Finite", "Physical", "Technical"],
            'correct': "Administrative",
            'explanation': "Both the policy and the instruction are administrative controls; rules and governance are administrative."
        },
        {
            'number': 22,
            'situation': "ISC2 publishes a Common Body of Knowledge (CBK) that IT security practitioners should be familiar with; this is recognized throughout the industry as a valuable resource for practitioners. Certifications can be issued for demonstrating expertise in this Common Body of Knowledge.",
            'question': "What kind of document is the Common Body of Knowledge?",
            'choices': ["Law", "Policy", "Procedure", "Standard"],
            'correct': "Standard",
            'explanation': "The Common Body of Knowledge is used throughout the industry, recognized among many people, countries and organizations. This is a standard."
        },
        {
            'number': 23,
            'situation': "The city of San Jose wants to ensure that all of its citizens are protected from malware, so the city council creates a rule that anyone caught creating and launching malware within the city limits will receive a fine and go to jail.",
            'question': "What kind of rule is this?",
            'choices': ["Law", "Policy", "Procedure", "Standard"],
            'correct': "Law",
            'explanation': "The city council is a governmental body making a legal mandate; this is a law."
        },
        {
            'number': 24,
            'situation': "The Triffid Corporation publishes a strategic overview of the company's intent to secure all the data the company possesses. This document is signed by Triffid's senior management.",
            'question': "What kind of document is this?",
            'choices': ["Law", "Policy", "Procedure", "Standard"],
            'correct': "Policy",
            'explanation': "This is an internal, strategic document, and is therefore a policy."
        },
        {
            'number': 25,
            'situation': "San Jose municipal code requires that all companies operating within city limits have a set of processes to ensure that employees are safe while working with hazardous materials. Triffid Corporation creates a checklist of activities that employees must follow while working with hazardous materials inside San Jose city limits.",
            'question': "Fill in the missing words: The municipal code is a ______, and the Triffid checklist is a ______.",
            'choices': ["Law, procedure", "Law, standard", "Policy, law", "Standard, law"],
            'correct': "Law, procedure",
            'explanation': "The municipal code was created by a governmental body and is a legal mandate; this is a law. The Triffid checklist is a detailed set of actions which must be used by Triffid employees in specific circumstances; this is a procedure."
        },
        {
            'number': 26,
            'situation': "The Payment Card Industry (PCI) Council is a committee made up of representatives from major credit card providers (Visa, Mastercard, American Express) in the United States. The PCI Council issues rules that merchants must follow if the merchants choose to accept payment via credit card. These rules describe best practices for securing credit card processing technology, activities for securing credit card information, and how to protect personal data of customers.",
            'question': "Which of the following describes this set of rules?",
            'choices': ["Law", "Policy", "Procedure", "Standard"],
            'correct': "Standard",
            'explanation': "This set of rules is known as the Data Security Standard, and it is accepted throughout the industry."
        },
        {
            'number': 27,
            'situation': "Hoshi is an ISC2 member who works for the Triffid Corporation as a data manager. Triffid needs a new firewall solution, and Hoshi is asked to recommend a product for Triffid to acquire and implement. Hoshi's cousin works for a firewall vendor; that vendor happens to make the best firewall available.",
            'question': "What should Hoshi do?",
            'choices': ["Disclose the relationship, but recommend the vendor/product", "Hoshi should ask to be recused from the task", "Recommend a different vendor/product", "Recommend the cousin's product"],
            'correct': "Disclose the relationship, but recommend the vendor/product",
            'explanation': "According to the third Canon of the ISC2 Code of Ethics, members are required to provide diligent and competent service to principals. Hoshi's principal here is Triffid, Hoshi's employer. It would be inappropriate for Hoshi to select the cousin's product solely based upon the family relationship; however, if the cousin's product is, in fact, the best choice for Triffid, then Hoshi should recommend that product. In order to avoid any appearance of impropriety or favoritism, Hoshi needs to declare the relationship when making the recommendation."
        },
        {
            'number': 28,
            'situation': "Olaf is a member of ISC2 and a security analyst for Triffid Corporation. During an audit, Olaf is asked whether Triffid is currently following a particular security practice. Olaf knows that Triffid is not adhering to that standard in that particular situation, but that saying this to the auditors will reflect poorly on Triffid.",
            'question': "What should Olaf do?",
            'choices': ["Ask ISC2 for guidance", "Ask supervisors for guidance", "Lie to the auditors", "Tell the auditors the truth"],
            'correct': "Tell the auditors the truth",
            'explanation': "The ISC2 Code of Ethics requires that members act honorably, honestly, justly, responsibly, and also advance and protect the profession. Both requirements dictate that Olaf should tell the truth to the auditors. While the Code also says that Olaf should provide diligent and competent service to principals, and Olaf's principal is Triffid in this case, lying does not serve Triffid's best long-term interests, even if the truth has some negative impact in the short term."
        },
        {
            'number': 29,
            'situation': "Aphrodite is a member of ISC2 and a data analyst for Triffid Corporation. While Aphrodite is reviewing user log data, Aphrodite discovers that another Triffid employee is violating the acceptable use policy and watching streaming videos during work hours.",
            'question': "What should Aphrodite do?",
            'choices': ["Inform ISC2", "Inform law enforcement", "Inform Triffid management", "Nothing"],
            'correct': "Inform Triffid management",
            'explanation': "Aphrodite is required by the ISC2 Code of Ethics to provide diligent and competent service to principals. This includes reporting policy violations to Triffid management (Triffid is the principal, in this case). A policy violation of this type is not a crime, so law enforcement does not need to be involved, and ISC2 has no authority over Triffid policy enforcement or employees."
        },
        {
            'number': 30,
            'situation': "Glena is an ISC2 member. Glena receives an email from a company offering a set of answers for an ISC2 certification exam.",
            'question': "What should Glena do?",
            'choices': ["Inform Glena's employer", "Inform ISC2", "Inform law enforcement", "Nothing"],
            'correct': "Inform ISC2",
            'explanation': "The ISC2 Code of Ethics requires that members advance and protect the profession; this includes protecting test security for ISC2 certification material. ISC2 (and every ISC2 member) has a vested interest in protecting test material, and countering any entity that is trying to undermine the validity of the certifications. This is, however, not a matter for law enforcement; if it turns out that law enforcement must be involved, ISC2 will initiate that activity. Glena's employer has no bearing on this matter."
        },
        {
            'number': 31,
            'situation': "You are reviewing log data from a router; there is an entry showing that a user sent traffic through the router at 11:45 a.m., local time, yesterday.",
            'question': "Which of the following does this exemplify?",
            'choices': ["Attack", "Event", "Incident", "Threat"],
            'correct': "Event",
            'explanation': "The example describes an event, which is any observable occurrence within the IT environment. (Any observable occurrence in a network or system. (Source: NIST SP 800-61 Rev 2)"
        },
        {
            'number': 32,
            'situation': "An attacker outside the organization attempts to gain access to the organization's internal files.",
            'question': "Which of the following does this scenario exemplify?",
            'choices': ["Disclosure", "Exploit", "Intrusion", "Publication"],
            'correct': "Intrusion",
            'explanation': "An intrusion is an attempt (successful or otherwise) to gain unauthorized access."
        },
        {
            'number': 33,
            'situation': "",
            'question': "Who approves the incident response policy?",
            'choices': ["ISC2", "senior management", "The investors", "The security manager"],
            'correct': "senior management",
            'explanation': "The organization's senior management are the only entities authorized to accept risk on behalf of the organization, and therefore all organizational policies must be approved by senior management."
        },
        {
            'number': 34,
            'situation': "",
            'question': "Which of the following are NOT typically involved in incident detection?",
            'choices': ["Automated Tools", "Regulators", "Security Analysis", "Users"],
            'correct': "Regulators",
            'explanation': "Typically, regulators do not detect incidents nor alert organizations to the existence of incidents."
        },
        {
            'number': 35,
            'situation': "",
            'question': "What is the goal of Business Continuity efforts?",
            'choices': ["Ensure all IT systems continue to operate", "Impress customers", "Keep critical business functions operational", "Save money"],
            'correct': "Keep critical business functions operational",
            'explanation': "Business Continuity efforts are about sustaining critical business functions during periods of potential interruption, such as emergencies, incidents, and disasters."
        },
        {
            'number': 36,
            'situation': "",
            'question': "Which of the following is likely to be included in the business continuity plan?",
            'choices': ["Alternate work areas for personnel affected by a natural disaster", "Last year's budget information", "Log data from all systems", "The organization's strategic security approach"],
            'correct': "Alternate work areas for personnel affected by a natural disaster",
            'explanation': "The business continuity plan should include provisions for alternate work sites, if the primary site is affected by an interruption, such as a natural disaster."
        },
        {
            'number': 37,
            'situation': "",
            'question': "What is the MOST important goal of a business continuity effort?",
            'choices': ["Ensure all business activities are preserved during a potential disaster", "Ensure all IT systems function during a potential interruption", "Ensure the organization survives a disaster", "Preserve health and human safety"],
            'correct': "Preserve health and human safety",
            'explanation': "In all security efforts, preserving health and human safety is paramount and takes precedence over anything else."
        },
        {
            'number': 38,
            'situation': "",
            'question': "What is the overall objective of a disaster recovery (DR) effort?",
            'choices': ["Enhance public perception of the organization", "Preserve critical business functions during a disaster", "Return to normal, full operations", "Save money"],
            'correct': "Return to normal, full operations",
            'explanation': "DR efforts are intended to return the organization to normal, full operations."
        },
        {
            'number': 39,
            'situation': "",
            'question': "What is the risk associated with resuming full normal operations too soon after a DR effort?",
            'choices': ["Investors might be upset", "Regulators might disapprove", "The danger posed by the disaster might still be present", "The organization could save money"],
            'correct': "The danger posed by the disaster might still be present",
            'explanation': "Resuming full normal operations too soon after a disaster might mean personnel are put in danger by whatever affects the disaster caused."
        },
        {
            'number': 40,
            'situation': "",
            'question': "What is the risk associated with delaying resumption of full normal operations after a disaster?",
            'choices': ["A new disaster might emerge", "Competition", "People might be put in danger", "The impact of running alternate operations for extended periods"],
            'correct': "The impact of running alternate operations for extended periods",
            'explanation': "Alternate operations are typically more costly than normal operations, in terms of impact to the organization; extended alternate operations could harm the organization as much as a disaster."
        },
        {
            'number': 41,
            'situation': "Gelbi is a Technical Support analyst for Triffid, Inc. Gelbi sometimes is required to install or remove software.",
            'question': "Which of the following could be used to describe Gelbi's account?",
            'choices': ["External", "Internal", "Privileged", "User"],
            'correct': "Privileged",
            'explanation': "A privileged account is an account that typically needs greater permissions than a basic user."
        },
        {
            'number': 42,
            'situation': "Guillermo logs on to a system and opens a document file.",
            'question': "Guillermo is an example of what?",
            'choices': ["The object", "The process", "The software", "The subject"],
            'correct': "The subject",
            'explanation': "Guillermo is the subject when he logs on to the system and opens a file."
        },
        {
            'number': 43,
            'situation': "",
            'question': "Which of the following is NOT an appropriate control to add to privileged accounts?",
            'choices': ["Increased auditing", "Increased logging", "Multi-factor authentication", "Security deposit"],
            'correct': "Security deposit",
            'explanation': "Privileged account holders usually are not asked for security deposits."
        },
        {
            'number': 44,
            'situation': "Prachi works as a database administrator for Triffid, Inc. Prachi is allowed to add or delete users, but is not allowed to read or modify the data in the database itself. When Prachi logs on to the system, an access control list (ACL) checks to determine which permissions he has.",
            'question': "In this situation, what is the ACL?",
            'choices': ["The firmware", "The object", "The rule", "The subject"],
            'correct': "The rule",
            'explanation': "The ACL, in this case, acts as the rule in the subject-object-rule relationship. It determines what Prachi is allowed to do, and what Prachi is not permitted to do."
        },
        {
            'number': 45,
            'situation': "Prachi works as a database administrator for Triffid, Inc. Prachi is allowed to add or delete users, but is not allowed to read or modify the data in the database itself. When Prachi logs on to the system, an access control list (ACL) checks to determine which permissions he has.",
            'question': "In this situation, Prachi represents what?",
            'choices': ["The file", "The object", "The rule", "The subject"],
            'correct': "The subject",
            'explanation': "Prachi is the subject in the subject-object-rule relationship. Prachi manipulates the database; this makes Prachi the subject."
        },
        {
            'number': 46,
            'situation': "Larry and Fern both work in the data center. In order to enter the data center to begin their workday, they must both present their own keys (which are different) to the key reader, before the door to the data center opens.",
            'question': "Which security concept is being applied in this situation?",
            'choices': ["Defense in depth", "Dual control", "Least privilege", "Segregation of duties"],
            'correct': "Dual control",
            'explanation': "This is an example of dual control, where two people, each with distinct authentication factors, must be present to perform a function."
        },
        {
            'number': 47,
            'situation': "",
            'question': "Which of the following is a biometric access control mechanism?",
            'choices': ["A badge reader", "A copper key", "A door locked by a voiceprint identifier", "A fence with razor tape on it"],
            'correct': "A door locked by a voiceprint identifier",
            'explanation': "A lock that opens according to a person's voice is a type of biometric access control."
        },
        {
            'number': 48,
            'situation': "",
            'question': "Which of the following is the BEST recommendation for all individuals visiting a secure facility?",
            'choices': ["Escort visitors", "Fingerprint visitors", "Photograph visitors", "Require visitors to wear protective gear"],
            'correct': "Escort visitors",
            'explanation': "In a secure facility, visitors should be escorted by an authorized person."
        },
        {
            'number': 49,
            'situation': "",
            'question': "All of the following are typically perceived as drawbacks to biometric systems, except:",
            'choices': ["Lack of accuracy", "Legality", "Potential privacy concerns", "Retention of physiological data past the point of employment"],
            'correct': "Lack of accuracy",
            'explanation': "Biometric systems can be extremely accurate, especially when compared with other types of access controls."
        },
        {
            'number': 50,
            'situation': "",
            'question': "A human guard monitoring a hidden camera could be considered which type of control?",
            'choices': ["Detective", "Deterrent", "Logical", "Preventive"],
            'correct': "Detective",
            'explanation': "The guard monitoring the camera can identify anomalous or dangerous activity; this is a detective control."
        },
        {
            'number': 51,
            'situation': "",
            'question': "Which of the following is a record of something that has occurred?",
            'choices': ["Biometric", "Firewall", "Law", "Log"],
            'correct': "Log",
            'explanation': "The description of a log is a record of something that has occurred."
        },
        {
            'number': 52,
            'situation': "Mila works for a government agency. All data in the agency is assigned a particular sensitivity level, called a classification. Every person in the agency is assigned a clearance level, which determines the classification of data each person can access and is controlled at the system level.",
            'question': "What is the access control model being implemented in Mila's agency?",
            'choices': ["DAC (discretionary access control)", "FAC (formal access control)", "MAC (mandatory access control)", "RBAC (role-based access control)"],
            'correct': "MAC (mandatory access control)",
            'explanation': "Mandatory Access Control is implemented at a system administrator level and cannot be adjusted for discretionary reasons."
        },
        {
            'number': 53,
            'situation': "",
            'question': "Which of the following would be considered a logical access control?",
            'choices': ["A chain attached to a laptop computer that connects it to furniture so it cannot be taken", "A fingerprint reader that allows an employee to access a laptop computer", "A fingerprint reader that allows an employee to enter a controlled area", "An iris reader that allows an employee to enter a controlled area"],
            'correct': "A fingerprint reader that allows an employee to access a laptop computer",
            'explanation': "Logical access controls limit who can gain user access to a device/system."
        },
        {
            'number': 54,
            'situation': "Trina and Doug both work at Triffid, Inc. Doug is having trouble logging in to the network. Trina offers to log in for Doug, using her credentials, so that Doug can get some work done.",
            'question': "What is the problem with this?",
            'choices': ["Anything either of them do will be attributed to Trina", "Doug is a bad person", "If Trina logs in for Doug, then Doug will never be encouraged to remember credentials without assistance", "It is against the law"],
            'correct': "Anything either of them do will be attributed to Trina",
            'explanation': "If two users are sharing one set of credentials, then the actions of both users will be attributed to that single account; the organization will be unable to discern exactly who performed which action, which can be troublesome if either user does something negligent or wrong."
        },
        {
            'number': 55,
            'situation': "Gary is unable to log in to the production environment. Gary tries three times and is then locked out of trying again for one hour.",
            'question': "Why could this be?",
            'choices': ["Gary is being punished", "Gary's actions look like an attack", "The network is tired", "Users remember their credentials if they are given time to think about it"],
            'correct': "Gary's actions look like an attack",
            'explanation': "Repeated login attempts can resemble an attack on the network; attackers might try to log in to a user's account multiple times, using different credentials, in a short time period, in an attempt to determine the proper credentials."
        },
        {
            'number': 56,
            'situation': "Suvid works at Triffid, Inc. When Suvid attempts to log in to the production environment, a message appears stating that he has to reset his password.",
            'question': "What may have occurred to cause this?",
            'choices': ["Someone hacked Suvid's machine", "Suvid broke the law", "Suvid made the manager angry", "Suvid's password has expired"],
            'correct': "Suvid's password has expired",
            'explanation': "Typically, users are required to reset passwords when the password has reached a certain age. Permanent passwords are more likely to be compromised or revealed."
        },
        {
            'number': 57,
            'situation': "Prina is a database manager. Prina is allowed to add new users to the database, remove current users, and create new usage functions for the users. Prina is not allowed to read the data in the fields of the database itself.",
            'question': "This is an example of what?",
            'choices': ["Alleviating threat access controls (ATAC)", "Discretionary access controls (DAC)", "Mandatory access controls (MAC)", "Role-based access controls (RBAC)"],
            'correct': "Role-based access controls (RBAC)",
            'explanation': "Role-based access controls often function in this manner, where the employee's job responsibilities dictate exactly which kinds of access the employee has. This also enforces the concept of least privilege."
        },
        {
            'number': 58,
            'situation': "Handel is a senior manager at Triffid, Inc., and is in charge of implementing a new access control scheme for the company. Handel wants to ensure that operational managers have the utmost personal choice in determining which employees get access to which systems/data.",
            'question': "Which method should Handel select?",
            'choices': ["Discretionary access controls (DAC)", "Mandatory access controls (MAC)", "Role-based access controls (RBAC)", "Security policy"],
            'correct': "Discretionary access controls (DAC)",
            'explanation': "DAC gives managers the most choice in determining which employees get access to which assets."
        },
        {
            'number': 59,
            'situation': "Handel is a senior manager at Triffid, Inc., and is in charge of implementing a new access control scheme for the company. Handel wants to ensure that employees transferring from one department to another, getting promoted, or cross-training to new positions can get access to the different assets they'll need for their new positions, in the most efficient manner.",
            'question': "Which method should Handel select?",
            'choices': ["Barbed wire", "Discretionary access controls (DAC)", "Mandatory access controls (MAC)", "Role-based access controls (RBAC)"],
            'correct': "Role-based access controls (RBAC)",
            'explanation': "RBAC is the most efficient way to assign permissions to users based on their job duties."
        },
        {
            'number': 60,
            'situation': "Handel is a senior manager at Triffid, Inc., and is in charge of implementing a new access control scheme for the company. Handel wants to ensure that employees who are assigned to new positions in the company do not retain whatever access they had in their old positions.",
            'question': "Which method should Handel select?",
            'choices': ["Discretionary access controls (DAC)", "Logging", "Mandatory access controls (MAC)", "Role-based access controls (RBAC)"],
            'correct': "Role-based access controls (RBAC)",
            'explanation': "RBAC can aid in reducing privilege creep, where employees who stay with the company for a long period of time might get excess permissions within the environment."
        },
        {
            'number': 61,
            'situation': "",
            'question': "Which term refers to the logical address of a device connected to the network or internet?",
            'choices': ["Geophysical address", "Internet Protocol (IP) address", "Media access control (MAC) address", "Terminal address"],
            'correct': "Internet Protocol (IP) address",
            'explanation': "The IP address is the logical address assigned to a device connected to a network or the Internet."
        },
        {
            'number': 62,
            'situation': "",
            'question': "What type of device filters network traffic in order to enhance overall security/performance?",
            'choices': ["Endpoint", "Firewall", "Laptop", "MAC (Media Access Control)"],
            'correct': "Firewall",
            'explanation': "Firewalls filter traffic in order to enhance the overall security or performance of the network, or both."
        },
        {
            'number': 63,
            'situation': "",
            'question': "What protocol should Barry use when he wants to upload a series of files to a web-based storage service?",
            'choices': ["FTP (File Transfer Protocol)", "SFTP (Secure File Transfer Protocol)", "SMTP (Simple Mail Transfer Protocol)", "SNMP (Simple Network Management Protocol)"],
            'correct': "SFTP (Secure File Transfer Protocol)",
            'explanation': "SFTP is designed specifically for this purpose."
        },
        {
            'number': 64,
            'situation': "",
            'question': "A type of device typically accessed by multiple users and often intended for a single purpose, such as managing email or web pages, is referred to as what?",
            'choices': ["Laptop", "Router", "Server", "Switch"],
            'correct': "Server",
            'explanation': "A server typically offers a specific service, such as hosting web pages or managing email, and is often accessed by multiple users."
        },
        {
            'number': 65,
            'situation': "Prina is a database manager. Prina is allowed to add new users to the database, remove current users, and create new usage functions for the users. Prina is not allowed to read the data in the fields of the database itself.",
            'question': "This is an example of what?",
            'choices': ["Alleviating threat access controls (ATAC)", "Discretionary access controls (DAC)", "Mandatory access controls (MAC)", "Role-based access controls (RBAC)"],
            'correct': "Role-based access controls (RBAC)",
            'explanation': "Role-based access controls often function in this manner, where the employee's job responsibilities dictate exactly which kinds of access the employee has. This also enforces the concept of least privilege."
        },
        {
            'number': 66,
            'situation': "",
            'question': "Carol is browsing the Web. Which of the following ports is she probably using?",
            'choices': ["12", "247", "80", "999"],
            'correct': "80",
            'explanation': "Port 80 is used for HTTP traffic, and HTTP is a Web-browsing protocol."
        },
        {
            'number': 67,
            'situation': "Cyril wants to ensure all the devices on his company's internal IT environment are properly synchronized.",
            'question': "Which of the following protocols would aid in this effort?",
            'choices': ["FTP", "HTTP (Hypertext Transfer Protocol)", "NTP (Network Time Protocol)", "SMTP (Simple Mail Transfer Protocol)"],
            'correct': "NTP (Network Time Protocol)",
            'explanation': "This is the purpose of NTP. FTP, SMTP and HTTP are incorrect; these do not serve the purpose of synchronization."
        },
        {
            'number': 68,
            'situation': "Ludwig is a security analyst at Triffid, Inc. Ludwig notices network traffic that might indicate an attack designed to affect the availability of the environment.",
            'question': "Which of the following might be the attack Ludwig sees?",
            'choices': ["An insider sabotaging the power supply", "DDOS (distributed denial of service)", "Exfiltrating stolen data", "Spoofing"],
            'correct': "DDOS (distributed denial of service)",
            'explanation': "DDOS is an availability attack, often typified by recognizable network traffic; either too much traffic to be processed normally, or malformed traffic."
        },
        {
            'number': 69,
            'situation': "Gary is an attacker. Gary is able to get access to the communication wire between Dauphine's machine and Linda's machine and can then surveil the traffic between the two when they're communicating.",
            'question': "What kind of attack is this?",
            'choices': ["DDOS", "On-path", "Physical", "Side channel"],
            'correct': "On-path",
            'explanation': "This is a textbook example of an on-path attack, where the attackers insert themselves between communicating parties."
        },
        {
            'number': 70,
            'situation': "Bert wants to add a flashlight capability to a smartphone. Bert searches the internet for a free flashlight app, and downloads it to the phone. The app allows Bert to use the phone as a flashlight, but also steals Bert's contacts list.",
            'question': "What kind of app is this?",
            'choices': ["DDOS", "On-path", "Side channel", "Trojan"],
            'correct': "Trojan",
            'explanation': "This is a textbook example of a Trojan horse application. Bert has intentionally downloaded the application with the intent to get a desired service, but the app also includes a hostile component Bert is unaware of."
        },
        {
            'number': 71,
            'situation': "Triffid, Inc., has many remote workers who use their own IT devices to process Triffid's information. The Triffid security team wants to deploy some sort of sensor on user devices in order to recognize and identify potential security issues.",
            'question': "Which of the following is probably most appropriate for this specific purpose?",
            'choices': ["Firewalls", "HIDS (host-based intrusion-detection systems)", "LIDS (logistical intrusion-detection systems)", "NIDS (network-based intrusion-detection systems)"],
            'correct': "HIDS (host-based intrusion-detection systems)",
            'explanation': "Host-based intrusion-detection systems are expressly designed for this purpose; each HIDS is installed on each endpoint machine."
        },
        {
            'number': 72,
            'situation': "Inbound traffic from an external source seems to indicate much higher rates of communication than normal, to the point where the internal systems might be overwhelmed.",
            'question': "Which security solution can often identify and potentially counter this risk?",
            'choices': ["Anti-malware", "Badge system", "Firewall", "Turnstile"],
            'correct': "Firewall",
            'explanation': "Firewalls can often identify hostile inbound traffic, and potentially counter it."
        },
        {
            'number': 73,
            'situation': "",
            'question': "What tool aggregates log data from multiple sources, typically analyzes it, and reports potential threats?",
            'choices': ["Anti-malware", "HIDS", "Router", "SIEM"],
            'correct': "SIEM",
            'explanation': "SIEM/SEM/SIM solutions are typically designed specifically for this purpose."
        },
        {
            'number': 74,
            'situation': "",
            'question': "What type of solution typically inspects outbound communications traffic to check for unauthorized exfiltration of sensitive/valuable information?",
            'choices': ["Anti-malware", "DLP (data loss prevention)", "Firewall", "NIDS (network-based intrusion-detection systems)"],
            'correct': "DLP (data loss prevention)",
            'explanation': "DLP solutions typically inspect outbound communications traffic to check for unauthorized exfiltration of sensitive/valuable information."
        },
        {
            'number': 75,
            'situation': "",
            'question': "What type of tool is used to monitor local devices with the aim of reducing potential threats from hostile software?",
            'choices': ["Anti-malware", "DLP (data loss prevention)", "Firewall", "NIDS (network-based intrusion-detection systems)"],
            'correct': "Anti-malware",
            'explanation': "This is the purpose of anti-malware solutions."
        },
        {
            'number': 76,
            'situation': "",
            'question': "Which activity is usually part of the configuration management process, but is also extremely helpful in countering potential attacks?",
            'choices': ["Annual budgeting", "Conferences with senior leadership", "The annual shareholders' meeting", "Updating and patching systems"],
            'correct': "Updating and patching systems",
            'explanation': "Keeping systems up to date is typically part of both the configuration management process and enacting best security practices."
        },
        {
            'number': 77,
            'situation': "",
            'question': "Which type of fire-suppression system is typically the SAFEST for humans?",
            'choices': ["Dirt", "Gaseous", "Oxygen-depletion", "Water"],
            'correct': "Water",
            'explanation': "Water is the safest fire-suppression system listed that is typically used."
        },
        {
            'number': 78,
            'situation': "",
            'question': "Which common cloud service model offers the customer the MOST control of the cloud environment?",
            'choices': ["Function as a Service (FaaS)", "Infrastructure as a service (IaaS)", "Platform as a service (PaaS)", "Software as a service (SaaS)"],
            'correct': "Infrastructure as a service (IaaS)",
            'explanation': "IaaS offers the customer the most control of the cloud environment, in terms of common cloud service models."
        },
        {
            'number': 79,
            'situation': "",
            'question': "What is the section of the IT environment that is closest to the external world; where we locate IT systems that communicate with the Internet?",
            'choices': ["DMZ", "MAC", "RBAC", "VLAN"],
            'correct': "DMZ",
            'explanation': "DMZ is what we often call this portion of the environment the demilitarized zone. VLAN is a way to segment portions of the internal network. MAC is the physical address of a given networked device. RBAC is an access control model."
        },
        {
            'number': 80,
            'situation': "",
            'question': "An IoT (Internet of Things) device is typically characterized by its effect on or use of which environment?",
            'choices': ["Development", "Internal", "Physical", "Remote"],
            'correct': "Physical",
            'explanation': "IoT devices typically have some interaction with the physical realm, either by having some physical effect (a vacuum cleaner, refrigerator, light) or by monitoring the physical environment itself (a camera, sensor, etc.)."
        },
        {
            'number': 81,
            'situation': "",
            'question': "What type of device is commonly advisable to have on the perimeter between two networks?",
            'choices': ["Camera", "Firewall", "IoT", "User laptop"],
            'correct': "Firewall",
            'explanation': "Firewalls are often useful to monitor/filter traffic between two networks."
        },
        {
            'number': 82,
            'situation': "",
            'question': "Which of the following describes when archiving is typically done?",
            'choices': ["When data has become illegal", "When data has lost all value", "When data is not needed for regular work purposes", "When data is ready to be destroyed"],
            'correct': "When data is not needed for regular work purposes",
            'explanation': "Archiving is the action of moving data from the production environment to long-term storage."
        },
        {
            'number': 83,
            'situation': "Every document owned by Triffid, Inc., whether hardcopy or electronic, has a clear, 24-point word at the top and bottom. Only three words can be used: 'Sensitive', 'Proprietary', and 'Public'.",
            'question': "Which concept does this demonstrate?",
            'choices': ["Inverting", "Labeling", "Privacy", "Secrecy"],
            'correct': "Labeling",
            'explanation': "Labeling is the practice of annotating assets with classification markings."
        },
        {
            'number': 84,
            'situation': "",
            'question': "To what data does security need to be provided?",
            'choices': ["All of the answers", "Illegal", "Private", "Restricted"],
            'correct': "All of the answers",
            'explanation': "All data needs some form of security; even data that is not sensitive (such as data intended for public view) needs protection to ensure availability."
        },
        {
            'number': 85,
            'situation': "",
            'question': "Hashing is often used to provide what?",
            'choices': ["Availability", "Confidentiality", "Integrity", "Value"],
            'correct': "Integrity",
            'explanation': "Hashing is used for integrity checks."
        },
        {
            'number': 86,
            'situation': "",
            'question': "If two people want to use asymmetric communication to conduct a confidential conversation, how many keys do they need?",
            'choices': ["11", "1", "4", "8"],
            'correct': "4",
            'explanation': "In asymmetric encryption, each party needs their own key pair (a public key and a private key) to engage in confidential communication."
        },
        {
            'number': 87,
            'situation': "",
            'question': "Which of the following describes the output of a hashing algorithm?",
            'choices': ["It's different when the same input is used", "It's the same characters", "It's the same language", "It's the same length"],
            'correct': "It's the same length",
            'explanation': "Hashing algorithms create output of a fixed length."
        },
        {
            'number': 88,
            'situation': "",
            'question': "What is the MOST crucial element of any security instruction program?",
            'choices': ["Ensure availability of IT systems", "Preserve health and human safety", "Preserve shareholder value", "Protect assets"],
            'correct': "Preserve health and human safety",
            'explanation': "This is the paramount rule in all security efforts."
        },
        {
            'number': 89,
            'situation': "",
            'question': "Which one of the following is a benefit of computer-based training (CBT)?",
            'choices': ["Expensive", "Interacting with other participants", "Personal interaction with instructor", "Scalable"],
            'correct': "Scalable",
            'explanation': "CBT is completely scalable, because it can be replicated uniformly for any number of users."
        },
        {
            'number': 90,
            'situation': "",
            'question': "An organization should keep on file a copy of every signed Acceptable Use Policy (AUP). To whom should a copy be issued?",
            'choices': ["Lawmakers", "The Public Relations office", "The regulators overseeing that industry", "The user who signed it"],
            'correct': "The user who signed it",
            'explanation': "The AUP is an agreement between the user and the organization, so both parties need to keep a copy of it."
        },
        {
            'number': 91,
            'situation': "",
            'question': "Why is the proper alignment of security policy and business goals within the organization important?",
            'choices': ["Bad security policy can be illegal", "Security is more important than business", "Security policy that conflicts with business goals can inhibit productivity", "Security should always be as strict as possible"],
            'correct': "Security policy that conflicts with business goals can inhibit productivity",
            'explanation': "Security is a support function in most organizations, not a business function; therefore, security policy must conform to business needs to avoid inhibiting productivity."
        },
        {
            'number': 92,
            'situation': "",
            'question': "What must an organization always be prepared to do when applying a patch?",
            'choices': ["Buy a new system", "Pay for the updated content", "Rollback", "Settle lawsuits"],
            'correct': "Rollback",
            'explanation': "Patches can sometimes cause unintended problems in the environment, so an organization must always be prepared to rollback the environment to the last known good state prior to when the patch was applied."
        },
        {
            'number': 93,
            'situation': "",
            'question': "Which of the following is used to ensure that configuration management activities are effective and enforced?",
            'choices': ["Baseline", "Identification", "Inventory", "Verification and audit"],
            'correct': "Verification and audit",
            'explanation': "Verification and audit are methods used to review the IT environment to ensure that configuration management activities have taken place and are achieving their intended purpose."
        },
        {
            'number': 94,
            'situation': "Triffid, Inc., wants to host streaming video files for the company's remote users, but wants to ensure that the data is protected while it's streaming.",
            'question': "Which method is probably BEST for this purpose?",
            'choices': ["Asymmetric encryption", "Hashing", "Symmetric encryption", "VLANs"],
            'correct': "Symmetric encryption",
            'explanation': "Symmetric encryption offers confidentiality of data with the least amount of processing overhead, which makes it the preferred means of protecting streaming data."
        },
        {
            'number': 95,
            'situation': "",
            'question': "What should security controls on log data reflect?",
            'choices': ["The local culture where the log data is stored", "The organization's commitment to customer service", "The price of the storage device", "The sensitivity of the source device"],
            'correct': "The sensitivity of the source device",
            'explanation': "Log data should be protected with security as high, or higher, than the security level of the systems or devices that log was captured from."
        },
        {
            'number': 96,
            'situation': "",
            'question': "How often should logs be reviewed?",
            'choices': ["Continually", "Every Thursday", "Once per calendar year", "Once per fiscal year"],
            'correct': "Continually",
            'explanation': "Log review should happen continually, in order to ensure detection efforts are optimized."
        },
        {
            'number': 97,
            'situation': "Dieter wants to send a message to Lupa and wants to be sure that Lupa knows the message has not been modified in transit.",
            'question': "Which technique/tool could Dieter use to assist in this effort?",
            'choices': ["Antivirus software", "Asymmetric encryption", "Hashing", "Symmetric encryption"],
            'correct': "Hashing",
            'explanation': "Hashing is a means to provide an integrity check."
        },
        {
            'number': 98,
            'situation': "",
            'question': "Where should log data be kept?",
            'choices': ["In airtight containers", "In an underground bunker", "On a device other than where it was captured", "On the device that the log data was captured from"],
            'correct': "On a device other than where it was captured",
            'explanation': "Log data can often be useful in diagnosing or investigating the device it was captured from; it is therefore useful to store the data away from the device where it was harvested, in case something happens to the source device."
        },
        {
            'number': 99,
            'situation': "",
            'question': "Which of the following describes data that is left behind on systems/media after normal deletion procedures have been attempted?",
            'choices': ["Fragments", "Packets", "Remanence", "Residue"],
            'correct': "Remanence",
            'explanation': "Data remanence is the term used to describe data left behind on systems/media after normal deletion procedures have been attempted."
        },
        {
            'number': 100,
            'situation': "",
            'question': "What should be done when data has reached the end of the retention period?",
            'choices': ["It should be archived", "It should be destroyed", "It should be enhanced", "It should be sold"],
            'correct': "It should be destroyed",
            'explanation': "At the end of the retention period, data should be securely destroyed."
        },
        {
            'number': 101,
            'situation': "",
            'question': "Data retention periods apply to which kind of data?",
            'choices': ["All of the answers", "Medical", "Secret", "Sensitive"],
            'correct': "All of the answers",
            'explanation': "All data should have specific retention periods (even though retention periods may differ for various types of data)."
        }
    ]
    
    # 全カード追加
    for q in questions:
        generator.add_card(
            question_number=q['number'],
            situation=q['situation'],
            question=q['question'],
            choices=q['choices'],
            correct_answer=q['correct'],
            explanation=q['explanation']
        )
    
    # 進捗保存とエクスポート
    generator.save_progress()
    generator.export_to_anki()
    
    print(f"バッチ処理完了: {len(generator.cards)}問")
    return generator

if __name__ == "__main__":
    generator = create_all_cards()
    print(f"総カード数: {len(generator.cards)}")
    print("\n次のスクリーンショットから問題4を分析してください。")