


class PrintController:
	PrintControllerPrintEntity = True
	PrintControllerPrintActions = True
	PrintControllerPrintCard = True
	PrintControllerPrintAura = True
	PrintControllerPrintCopy = True


def enable_print():
	PrintController.PrintControllerPrintEntity = True
	PrintController.PrintControllerPrintActions = True
	PrintController.PrintControllerPrintCard = True
	PrintController.PrintControllerPrintAura = True
	PrintController.PrintControllerPrintCopy = True



def disable_print():
	PrintController.PrintControllerPrintEntity = False
	PrintController.PrintControllerPrintActions = False
	PrintController.PrintControllerPrintCard = False
	PrintController.PrintControllerPrintAura = False
	PrintController.PrintControllerPrintCopy = False



def print_actions():
	return PrintController.PrintControllerPrintActions


def print_entity():
	return PrintController.PrintControllerPrintEntity


def print_card():
	return PrintController.PrintControllerPrintCard


def print_aura():
	return PrintController.PrintControllerPrintCard


def print_copy():
	return PrintController.PrintControllerPrintCopy
