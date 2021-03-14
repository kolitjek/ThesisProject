


class PrintController:
	PrintControllerPrintEntity = False
	PrintControllerPrintActions = False
	PrintControllerPrintCard = False


def enable_print():
	PrintController.PrintControllerPrintEntity = True
	PrintController.PrintControllerPrintActions = True
	PrintController.PrintControllerPrintCard = True


def disable_print():
	PrintController.PrintControllerPrintEntity = False
	PrintController.PrintControllerPrintActions = False
	PrintController.PrintControllerPrintCard = False


def print_actions():
	return PrintController.PrintControllerPrintActions


def print_entity():
	return PrintController.PrintControllerPrintEntity


def print_card():
	return PrintController.PrintControllerPrintCard
