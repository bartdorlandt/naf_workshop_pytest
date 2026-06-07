# Workshop FAQ: (Py)Test your Automation
**Proctor(s)**: Urs Baumann, Steinn Orvar Bjarnarson, Bart Dorlandt

---

## General Information

### 1. What is this workshop about?

Modern network automation is software engineering, yet many projects lack effective testing strategies. Rather than relying on lab or production systems for validation, we can test automation logic early, efficiently, and with predictable results.

This hands-on workshop introduces PyTest for network automation, focusing on testing business logic and mocking device or third-party interfaces. Participants will learn to design testable automation code, isolate external dependencies, and simulate network devices and APIs using mocks.

**Topics**:

- Designing testable automation code
- Separating business logic from device interaction
- PyTest fixtures and parametrization
- Mocking device drivers and third-party APIs
- Simulating failure scenarios (timeouts, auth errors, partial config pushes)
- Building fast, deterministic unit test suites
- Integrating PyTest into CI/CD workflows

This workshop is ideal for network automation engineers looking to build maintainable, scalable, and production-ready automation systems.

### 2. What experience level is required?

This workshop is designed for participants with an intermediate level of experience in Python. You should be comfortable working with Python and have some familiarity with network automation concepts. Prior experience with pytest or testing frameworks is beneficial but not strictly required.

---

## Pre-Workshop Preparation

### 3. What do I need to install before the workshop?

- **Python (version 3.12)**
- **Python venv**: To avoid messing up your local Python setup, you should be able to create a virtual Python environment or work in a dedicated container/VM. We highly recommend using `uv` for this, as it simplifies the process of managing virtual environments and dependencies. This workshop assumes you have `uv` installed and are familiar with its basic usage. If you haven't used `uv` before, please take some time to familiarize yourself with it before the workshop. You can find the documentation here: [uv Documentation](https://docs.astral.sh/uv/).
- **Unix**: It is recommended that you work on a Unix-based operating system like Linux, MacOS, or WSL.
- **Libraries**: pytest, pytest-mock (will be installed as part of the setup)
- **IDE**: You can use the IDE you desire. The proctors are most comfortable with VSCode.

By using `uv sync`, you are ready for the workshop. (`uv` will create a virtual environment and install the required dependencies based on the `uv.lock` file.)

### 4. Are there any pre-reading materials?

There is no mandatory pre-reading, but it does not harm to familiarize yourself with the official documentation of the libraries we will cover:

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-mock](https://pytest-mock.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [uv](https://docs.astral.sh/uv/)

### 5. Do I need to bring any equipment?

Yes, please bring a laptop with `uv` and `docker` pre-installed. Ensure that your laptop is configured with the appropriate permissions to install and run software.

Ensure you ran `uv sync` to create the virtual environment.

### 6. Can I use GitHub Codespaces?

Yes. All the labs work well with GitHub Codespaces. Make sure your free quota is not exceeded.

---

## Own Ideas

### 7. Can I implement my own ideas?

Definitely, it is appreciated to consider how you can apply the learned material to your specific use case. However, time is limited, and the proctors cannot focus on each idea in detail.

### 8. Lab access?

No external lab access is required. This workshop focuses on testing automation code locally using mocks and fixtures. All exercises run entirely on your local machine without requiring network device access.

---

## Technical Questions

### 9. Will the workshop be hands-on?

Yes! This is a practical, hands-on workshop. You will be actively writing and running Python code and tests throughout the session.

---

## Additional Information

### 10. Who do I contact if I have questions before the workshop?

For any questions or concerns prior to the workshop, feel free to use the Slack channel [`#ac5-ws-b4-pytest`](https://networkautomationfrm.slack.com/archives/C0AUFJ4KG92) or contact a proctor directly through the Network Automation Forum Slack.

### 11. What if I cannot keep up with the pace of the workshop?

This workshop is designed for an intermediate skill level, but don't worry if you fall behind. The proctors are happy to assist during the session, and you can also use breaks to catch up. Additionally, each section includes checkpoint solutions to help you stay on track. The goal is to ensure everyone can follow along and gain hands-on experience.
